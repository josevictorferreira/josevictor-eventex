from django.core import mail
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

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Jose Victor', cpf='12345678901',
                    email='jose@mailinator.com', phone='43-3358-6180')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        '''Valid POST should redirect to /inscricao/'''
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'tinhodunk@gmail.com'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['tinhodunk@gmail.com', 'jose@mailinator.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):

        self.assertIn('Jose Victor', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('jose@mailinator.com', self.email.body)
        self.assertIn('43-3358-6180', self.email.body)

class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
        self.form = self.response.context['form']

    def test_post(self):
        '''Invalid POST shoeld not redirect'''
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)

class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        self.data = dict(name='Jose Victor', cpf='12345678901',
                         email='jose@mailinator.com', phone='43-3358-5544')
        self.response = self.client.post('/inscricao/', self.data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscricao realizada com sucesso!')

