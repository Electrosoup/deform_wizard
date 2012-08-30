import unittest
from mock import patch
from mock import Mock
from pyramid import testing
from pyramid.exceptions import ConfigurationError


class Wizard(unittest.TestCase):

    def setUp(self):

        self.config = testing.setUp()

    def tearDown(self):

        testing.tearDown()

    def test_init_wizrd(self):

        from deform_wizard import FormWizard

        import colander

        class Name(colander.MappingSchema):

            name = colander.SchemaNode(colander.String('UTF-8'))

            title = colander.SchemaNode(colander.String('UTF-8'))

            description = colander.SchemaNode(colander.String('UTF-8'))

            first_name = colander.SchemaNode(colander.String('UTF-8'))

            surname = colander.SchemaNode(colander.String('UTF-8'))

        class Address (colander.MappingSchema):

            name = colander.SchemaNode(colander.String('UTF-8'))

            title = colander.SchemaNode(colander.String('UTF-8'))

            description = colander.SchemaNode(colander.String('UTF-8'))

            address_one = colander.SchemaNode(colander.String('UTF-8'))

            address_two = colander.SchemaNode(colander.String('UTF-8'))

            town_city = colander.SchemaNode(colander.String('UTF-8'))

            country = colander.SchemaNode(colander.String('UTF-8'))

            post_code = colander.SchemaNode(colander.String('UTF-8'))

        from pyramid.testing import DummyRequest

        request = DummyRequest()

        name = Name().bind(request=request)

        address = Address().bind(request=request)

        wiz = FormWizard('wizard', name, address)

        wiz(request)
