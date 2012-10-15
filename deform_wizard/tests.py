import unittest

from pyramid import testing

from mock import Mock


class Wizard(unittest.TestCase):

    def setUp(self):

        from pyramid.testing import DummyRequest

        self.request = DummyRequest()

        self.config = testing.setUp()

        self.request = DummyRequest()

    def tearDown(self):

        testing.tearDown()

    def get_csrf_request(self, post=None):

        csrf = 'abc'

        if not u'csrf_token' in post.keys():

            post.update({

                'csrf_token': csrf

            })

        request = testing.DummyRequest(post)

        request.session = testing.DummySession()

        csrf_token = Mock()

        csrf_token.return_value = csrf

        request.session.get_csrf_token = csrf_token

        return request

    def _get_target_class(self):

        from deform_wizard import FormWizard

        return FormWizard

    def _make_one(self, request):

        from deform_wizard import CSRFSchema

        import colander

        class Name(CSRFSchema):

            name = colander.SchemaNode(colander.String('UTF-8'))

        class Address (CSRFSchema):

            address_one = colander.SchemaNode(colander.String('UTF-8'))

            address_two = colander.SchemaNode(colander.String('UTF-8'))

        klass = self._get_target_class()

        name = Name().bind(request=request)

        address = Address().bind(request=request)

        return klass('wizard', name, address)

    def test_init_wizard(self):

        wiz = self._make_one(self.request)

        self.assertEqual(len(wiz.schemas), 2)

    def test_render_wizard(self):

        from deform_wizard import FormWizardView

        wiz = self._make_one(self.request)

        form = FormWizardView(wiz)(self.request)

        self.assertIn('form', form.keys())

    def test_validation_pass(self):

        from deform_wizard import FormWizardView

        request = self.get_csrf_request(post={'name': 'simon'})

        wiz = self._make_one(request)

        form = FormWizardView(wiz)(request)

        self.assertNotIn('errorMsg', form['form'])

    def test_validation_fail(self):

        from deform_wizard import FormWizardView

        request = self.get_csrf_request(post={'dave': 'nonsense'})

        wiz = self._make_one(request)

        form = FormWizardView(wiz)(request)

        self.assertIn('errorMsg', form['form'])

    def test_step_forwards(self):

        from deform_wizard import FormWizardView

        request = self.get_csrf_request(post={'name': 'simon', 'Next': 'next'})

        wiz = self._make_one(request)

        form = FormWizardView(wiz)(request)

        self.assertIn('address_one', form['form'])

    def test_step_backwards(self):

        from deform_wizard import FormWizardView

        request = self.get_csrf_request(post={'name': 'simon', 'Next': 'next'})

        wiz = self._make_one(request)

        form = FormWizardView(wiz)(request)

        new_request = self.get_csrf_request(
            post={'address_one': 'sasas',
            'address_two': 'ewewe',
            'Previous': 'previous'}
            )

        new_request.session = request.session

        form = FormWizardView(wiz)(new_request)

        self.assertIn('simon', form['form'])

    def test_step_finish(self):

        from deform_wizard import FormWizardView

        request = self.get_csrf_request(post={'name': 'simon', 'Next': 'next'})

        wiz = self._make_one(request)

        form = FormWizardView(wiz)(request)

        new_request = self.get_csrf_request(
            post={'address_one': 'sasas',
            'address_two': 'ewewe',
            'Finish': 'finish'}
            )

        new_request.session = request.session

        form = FormWizardView(wiz)(new_request)

        self.assertEqual(2, len(form['wizard_data']))
