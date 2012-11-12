import deform
import deform.form
import deform.exception
import deform.widget
import colander


class WizardState(object):

    def __init__(self, request, wizard_name):

        self.wizard_name = wizard_name

        self.request = request

    def _get_wizard_data(self):

        session = self.request.session

        wizdatas = session.setdefault('deform_wizard.wizards', {})

        wizdata = wizdatas.get(self.wizard_name, None)

        if wizdata is None:

            wizdata = {}

            wizdatas[self.wizard_name] = wizdata

            session.changed()

        return wizdata

    def clear(self):

        wizdata = self._get_wizard_data()

        wizdata.clear()

        self.request.session.changed()

    def get_step_num(self):

        step = self.request.GET.get('step')

        if step is not None:

            step = int(step)

            self.set_step_num(step)

        else:

            wizdata = self._get_wizard_data()

            step = wizdata.get('step', 0)

        return int(step)

    def set_step_num(self, num):

        wizdata = self._get_wizard_data()

        wizdata['step'] = num

        self.request.session.changed()

    def get_step_states(self):

        wizdata = self._get_wizard_data()

        states = wizdata.setdefault('states', {})

        return states

    def get_current_step(self):

        if self.get_step_num() in self.get_step_states():

            return self.get_step_states()[self.get_step_num()]

        return {}

    def set_step_state(self, num, state):

        states = self.get_step_states()

        states[num] = state

        self.request.session.changed()

    def decrement_step(self):

        step = self.get_step_num()

        if step > 0:

            self.set_step_num(step - 1)

    def increment_step(self):

        step = self.get_step_num()

        self.set_step_num(step + 1)

    def set_state(self, state):

        step = self.get_step_num()

        self.set_step_state(step, state)


class FormWizardView(object):

    def __init__(self, wizard):

        self.wizard = wizard

    def __call__(self, request):

        self.request = request

        form = self._gen_form()

        if request.POST:

            ws = WizardState(self.request, self.wizard.name)

            controls = request.POST.items()

            try:

                values = form.validate(controls)

            except deform.exception.ValidationFailure as e:

                return{'form': e.render()}

            ws.set_state(values)

            if 'Next' in request.POST:

                ws.increment_step()

                form = self._gen_form()

                values = ws.get_current_step()

                return {'form': form.render(values)}

            if 'Previous' in request.POST:

                ws = WizardState(self.request, self.wizard.name)

                ws.decrement_step()

                form = self._gen_form()

                values = ws.get_current_step()

                return {'form': form.render(values)}

            if 'Finish' in request.POST:

                states = ws.get_step_states()

                ws.clear()

                for i in states.keys():

                    del states[i]['csrf_token']

                return {'wizard_data': states}

        return {'form': form.render()}

    def _gen_form(self):

        buttons = []

        ws = WizardState(self.request, self.wizard.name)

        step = ws.get_step_num()

        schema = self.wizard.schemas[step]

        if step > 0:

            buttons.append('Previous')

        if step < len(self.wizard.schemas) - 1:

            buttons.append('Next')

        if step == len(self.wizard.schemas) - 1:

            buttons.append('Finish')

        return deform.Form(schema, buttons=buttons)


class FormWizard(object):

    def __init__(self, name, *schemas):

        self.name = name

        self.schemas = schemas

    def __call__(self, request):

        view = FormWizardView(self)

        result = view(request)

        return result


@colander.deferred
def deferred_csrf_value(node, kw):

    return kw['request'].session.get_csrf_token()


@colander.deferred
def deferred_csrf_validator(node, kw):

    def csrf_validate(node, value):

        if value != kw['request'].session.get_csrf_token():

            raise colander.Invalid(node,
                    ('Invalid cross-site scripting token'))

    return csrf_validate


class CSRFSchema(colander.Schema):
    """
    Schema base class which generates and validates a CSRF token
    automatically.  You must use it like so:

    .. code-block:: python

      from pyramid_deform import CSRFSchema
      import colander

      class MySchema(CRSFSchema):
          my_value = colander.SchemaNode(colander.String())

      And in your application code, *bind* the schema, passing the request
      as a keyword argument:

      .. code-block:: python

        def aview(request):
            schema = MySchema().bind(request=request)

      In order for the CRSFSchema to work, you must configure a *session
      factory* in your Pyramid application.
    """
    csrf_token = colander.SchemaNode(

        colander.String(),

        widget=deform.widget.HiddenWidget(),

        default=deferred_csrf_value,

        validator=deferred_csrf_validator,

        )
