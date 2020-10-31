import pytest

@pytest.fixture()
def fixture_student():
    from src.StudentBD import StudentDB
    db = StudentDB()
    db.connect('data/students.json')
    return db