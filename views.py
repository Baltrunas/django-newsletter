# -*- coding: utf-8 -*
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from newsletter.models import Subscriber
from newsletter.forms import SubscribeForm
from newsletter.forms import SettingsForm
from newsletter.forms import SettingsObjectForm

context = {}


def subscribe(request):
	context['title'] = _('News Letter')
	if request.method == 'POST':
		context['form'] = SubscribeForm(request.POST)
		if context['form'].is_valid():
			context['formdate'] = context['form'].cleaned_data

			new_subscriber = Subscriber(
				gender=context['formdate'].get('gender', None),
				name=context['formdate'].get('name', None),
				surname=context['formdate'].get('surname', None),
				email=context['formdate'].get('email', None)
			)
			new_subscriber.save()
			new_subscriber.categories = context['formdate'].get('categories', None)
			new_subscriber.save()

			context['new_subscriber'] = new_subscriber

			email = context['formdate'].get('email', None)
			subject = _('Subscribe')
			send_from = '%s <%s>' % ('Ronis', 'no-reaply@ronis.de')
			subscribe_template = render_to_string('newsletter/email_subscribe.html', context)
			subscribe_email = EmailMultiAlternatives(subject, subscribe_template, send_from, [email])
			subscribe_email.attach_alternative(subscribe_template, "text/html")
			subscribe_email.send()
			context['ok'] = True
	else:
		context['ok'] = False
		context['form'] = SubscribeForm()
	return render_to_response('newsletter/subscribe.html', context, context_instance=RequestContext(request))


def settings(request, key):
	context['title'] = _('Subscribe Settings')
	subscriber = Subscriber.objects.get(key=key)
	if request.method == 'POST':
		context['form'] = SettingsForm(request.POST)
		if context['form'].is_valid():
			context['formdate'] = context['form'].cleaned_data
			if context['formdate'].get('subscribed', False) == 'True':
				subscriber.subscribed = True
			else:
				subscriber.subscribed = False

			if context['formdate'].get('gender', False) == 'True':
				subscriber.gender = True
			else:
				subscriber.gender = False

			subscriber.name = context['formdate'].get('name', None)
			subscriber.surname = context['formdate'].get('surname', None)
			subscriber.categories = context['formdate'].get('categories', None)
			subscriber.save()

	context['form'] = SettingsObjectForm(subscriber)
	return render_to_response('newsletter/settings.html', context, context_instance=RequestContext(request))
