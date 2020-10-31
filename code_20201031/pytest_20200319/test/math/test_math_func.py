def test_add(fixture_add):
    assert fixture_add(3, 3) == 6
    assert fixture_add(3) == 3

def test_product(fixture_product):
    assert fixture_product(3, 3) == 9
    assert fixture_product(3) == 3