"""This is the module doc"""
import pytest

pytestmark = [
    pytest.mark.module_mark,
    pytest.mark.module_mark_2,
    pytest.mark.pytest_doc(name="Test Docs"),
]


@pytest.mark.class_marker
@pytest.mark.pytest_doc(name="Test Class")
class TestClass:
    """This is the class doc"""

    @pytest.mark.func_mark_a("foo")
    def test_func_a(self):
        """This is the doc for test_func_a"""
        assert 1

    @pytest.mark.kwarg_mark(goo="bla")
    def test_func_b(self):
        """This is the doc for test_func_b"""
        assert 1
