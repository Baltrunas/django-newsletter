# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Input
from django.utils.translation import ugettext_lazy as _
from newsletter.models import Category


class Html5EmailInput(Input):
	input_type = 'email'


class SubscribeForm(forms.Form):
	categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, label=_('Categories'), queryset=Category.objects.filter(public=True))

	email = forms.EmailField(max_length=128, label=_('E-Mail'), widget=Html5EmailInput(attrs={'required': 'required', 'placeholder': _('no-reaply@example.com')}))

	gender = forms.TypedChoiceField(
		label=_('Gender'),
		coerce=lambda x: True if x == 'True' else False,
		initial=False,
		choices=((False, _('Women')), (True, _('Man'))),
		widget=forms.RadioSelect
	)

	name = forms.CharField(max_length=512, required=False, label=_('Name'), widget=forms.TextInput(attrs={'placeholder': _('Private')}))
	surname = forms.CharField(max_length=512, required=False, label=_('Surname'), widget=forms.TextInput(attrs={'placeholder': _('Person')}))


class SettingsForm(forms.Form):
	categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, label=_('Categories'), queryset=Category.objects.filter(public=True))
	subscribed = forms.TypedChoiceField(
		label=_('Subscribed'),
		# coerce=lambda x: True if x == 'True' else False,
		choices=((True, _('Yes')), (False, _('No'))),
		widget=forms.RadioSelect
	)
	gender = forms.TypedChoiceField(
		label=_('Gender'),
		# coerce=lambda x: True if x == 'True' else False,
		choices=((True, _('Man')), (False, _('Women'))),
		widget=forms.RadioSelect
	)
	name = forms.CharField(max_length=512, label=_('Name'), widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Private')}))
	surname = forms.CharField(max_length=512, label=_('Surname'), widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Person')}))


class SettingsObjectForm(SettingsForm):
	def __init__(self, subscriber, *args, **kwargs):
		super(SettingsObjectForm, self).__init__(*args, **kwargs)
		self.fields['categories'].initial = subscriber.categories.all()
		self.fields['subscribed'].initial = subscriber.subscribed
		self.fields['gender'].initial = subscriber.gender
		self.fields['name'].initial = subscriber.name
		self.fields['surname'].initial = subscriber.surname
