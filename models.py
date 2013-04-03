# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import SafeUnicode
import hashlib
from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=512, verbose_name=_('Name'))
	description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
	phone = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('Phone'))

	from_name = models.CharField(max_length=128, verbose_name=_('From name'))
	from_email = models.EmailField(max_length=128, verbose_name=_('From E-Mail'))

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __unicode__(self):
		return SafeUnicode(self.name)

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')


class Subscriber(models.Model):
	GENDER_CHOICES = (
		(True, _('Man')),
		(False, _('Women')),
	)
	gender = models.BooleanField(_('Gender'), default=False, choices=GENDER_CHOICES)
	name = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('Name'))
	surname = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('Surname'))
	email = models.EmailField(verbose_name=_('E-Mail'), max_length=128)
	subscribed = models.BooleanField(_('Subscribed'), default=True)
	key = models.CharField(max_length=32, verbose_name=_('Key'), editable=False, default='')

	categories = models.ManyToManyField(Category, related_name='subscribers', verbose_name=_('Category'), blank=True)

	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def is_subscribed(self, email):
		try:
			return self.objects.get(email=email).subscribed
		except:
			return False

	def save(self, *args, **kwargs):
		super(Subscriber, self).save(*args, **kwargs)
		if not self.key:
			self.key = hashlib.md5(self.email + str(self.created_at)).hexdigest()
			super(Subscriber, self).save(*args, **kwargs)

	def __unicode__(self):
		return '<%s> - [%s]' % (self.email, self.created_at)

	class Meta:
		ordering = ['created_at', 'email']
		verbose_name = _('Subscriber')
		verbose_name_plural = _('Subscribers')


class Mesage(models.Model):
	subject = models.CharField(max_length=512, verbose_name=_('Subject'))
	category = models.ForeignKey(Category, related_name='mesages', default=1, verbose_name=_('Category'))
	body = models.TextField(verbose_name=_('Body'))
	send_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)

	def __unicode__(self):
		return '#%s - %s' % (self.pk, self.subject)

	def save(self, *args, **kwargs):
		super(Mesage, self).save(*args, **kwargs)
		context = {}
		for subscriber in self.category.subscribers.filter(subscribed=True):
			context['subscriber'] = subscriber
			context['mesage'] = self
			send_from = '%s <%s>' % (self.category.from_name, self.category.from_email)
			newsletter_template = render_to_string('newsletter/email_newsletter.html', context)
			newsletter_email = EmailMultiAlternatives(self.subject, newsletter_template, send_from, [subscriber.email])
			newsletter_email.attach_alternative(newsletter_template, "text/html")
			newsletter_email.send()

	class Meta:
		ordering = ['-send_at']
		verbose_name = _('Mesage')
		verbose_name_plural = _('Mesages')
