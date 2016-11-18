import pytest


@pytest.fixture
def browser():
    import mock
    browser = mock.MagicMock()

    from zope.interface import alsoProvides
    from pypom.splinter_driver import ISplinter
    alsoProvides(browser, ISplinter)
    return browser


def test_meta(browser):
    """ test metaclass """
    import colander

    from pypom_form.widgets import StringWidget

    class MyStringWidget(StringWidget):
        pass

    class BaseFormSchema(colander.MappingSchema):
        title = colander.SchemaNode(colander.String(),
                                    selector=('id', 'id1'))

    class SubFormSchema(BaseFormSchema):
        name = colander.SchemaNode(colander.String(),
                                   selector=('id', 'id2'),
                                   pwidget=MyStringWidget(
                                       kwargs={'test': 1}))

    import pypom
    from pypom_form.meta import PageEditMetaclass

    class SubFormPage(pypom.Page):
        __metaclass__ = PageEditMetaclass
        schema_factory = SubFormSchema

    subform = SubFormPage(browser)
    import mock

    with mock.patch(
            'pypom_form.widgets.StringWidget.get_input_element') \
            as get_input_element:
        get_input_element.configure_mock(**{'return_value.value': 'the title'})
        assert subform.title == 'the title'

    with mock.patch(
            'pypom_form.widgets.StringWidget.get_input_element') \
            as get_input_element:
        get_input_element.configure_mock(**{'return_value.value': 'the name'})
        assert subform.name == 'the name'
