import pytest

@pytest.fixture()
def fixture_add():
    from src.math_func import add
    return add

@pytest.fixture()
def fixture_product():
    from src.math_func import product
    return product