def test_get_data(fixture_student):
    markio = fixture_student.get_data('Markio')
    assert markio['name'] == 'Markio' 