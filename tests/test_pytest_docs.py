import pytest

TEST_SUITE = """
'''This is the module doc'''
import pytest

pytestmark = [
    pytest.mark.module_mark,
    pytest.mark.module_mark_2,
    pytest.mark.pytest_doc(name="Test Docs"),
]


@pytest.mark.class_marker
@pytest.mark.pytest_doc(name="Test Class")
class TestClass:
    '''This is the class doc'''

    @pytest.mark.func_mark_a("foo")
    def test_func_a(self):
        '''This is the doc for test_func_a'''
        assert 1

    @pytest.mark.kwarg_mark(goo="bla")
    def test_func_b(self):
        '''This is the doc for test_func_b'''
        assert 1
"""


@pytest.mark.parametrize(
    "file_type, expected_file",
    [("md", "markdown_sanity.md"), ("rst", "rst_sanity.rst")],
)
def test_formatter_sanity(testdir, tmpdir, file_type, expected_file, expected_output):
    path = tmpdir.join("doc.{}".format(file_type))
    testdir.makepyfile(TEST_SUITE)
    testdir.runpytest("--docs", str(path), "--doc-type", file_type)
    assert path.read() == expected_output(expected_file)

def test_custom_formatter(testdir, tmpdir,):
    file_type = "custom"
    path = tmpdir.join("doc.{}".format(file_type))
    testdir.makepyfile(TEST_SUITE)
    testdir.runpytest(
        "--docs", str(path),
        "--doc-type", file_type,
        "--custom-formatter-path", "tests.formatters_for_test.empty_formatter"
    )
    assert "#" not in path.read()
