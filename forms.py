# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Input
from django.utils.translation import ugettext_lazy as _
from newsletter.models import Category


class Html5EmailInput(Input):
	input_type = 'email'


class SubscribeForm(forms.Form):
	categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Category.objects.filter(public=True))

	email = forms.EmailField(max_length=128, widget=Html5EmailInput(attrs={'required': 'required', 'placeholder': _('no-reaply@example.com')}))

	gender = forms.TypedChoiceField(
		coerce=lambda x: True if x == 'True' else False,
		initial=False,
		choices=((False, _('Women')), (True, _('Man'))),
		widget=forms.RadioSelect
	)

	name = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Private')}))
	surname = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Person')}))


class SettingsForm(forms.Form):
	categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Category.objects.filter(public=True))
	subscribed = forms.TypedChoiceField(
		# coerce=lambda x: True if x == 'True' else False,
		choices=((False, _('No')), (True, _('Yes'))),
		widget=forms.RadioSelect
	)
	gender = forms.TypedChoiceField(
		# coerce=lambda x: True if x == 'True' else False,
		choices=((False, _('Women')), (True, _('Man'))),
		widget=forms.RadioSelect
	)
	name = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Private')}))
	surname = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'required': 'required', 'placeholder': _('Person')}))


class SettingsObjectForm(SettingsForm):
	def __init__(self, subscriber, *args, **kwargs):
		super(SettingsObjectForm, self).__init__(*args, **kwargs)
		self.fields['categories'].initial = subscriber.categories.all()
		self.fields['subscribed'].initial = subscriber.subscribed
		self.fields['gender'].initial = subscriber.gender
		self.fields['name'].initial = subscriber.name
		self.fields['surname'].initial = subscriber.surname
