import pytest


@pytest.mark.parametrize(
    "file_type, expected_file",
    [("md", "markdown_sanity.md"), ("rst", "rst_sanity.rst")],
)
def test_formatter_sanity(testdir, tmp_path, file_type, expected_file, expected_output):
    path = tmp_path / "doc.{}".format(file_type)
    testdir.copy_example("test_suite.py")
    testdir.runpytest("--docs", str(path), "--doc-type", file_type)
    assert path.read_text() == expected_output(expected_file)
