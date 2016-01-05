from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
        self.form = self.response.context['form']

    def test_get(self):
        '''Get /inscricao/ must return status code 200'''
        self.assertEqual(200, self.response.status_code)

    def test_tempalte(self):
        '''Must use subscriptions/subscription_form.html'''
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        '''Html must contain input tags'''
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        '''Html must contain csrf'''
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        '''Form must have 4 fields'''
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(self.form.fields))