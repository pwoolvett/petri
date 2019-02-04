from behave import given, when, then

from petri import settings


@given("we have behave installed2")
def behave_installed(context):
    pass


@given("this feature2")
def feature_loaded(context):
    pass


@when("we implement a test2")
def sample_assert(context):
    pass


@then("behave will test it for us!2")
def use_context_data(context):
    assert 0, settings.DOTENV_LOCATION
