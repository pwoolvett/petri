from behave import given, when, then


@given("we have behave installed")
def behave_installed(context):
    pass


@given("this feature")
def feature_loaded(context):
    pass


@when("we implement a test")
def sample_assert(context):
    assert True is not False


@then("behave will test it for us!")
def use_context_data(context):
    assert context.failed is False
