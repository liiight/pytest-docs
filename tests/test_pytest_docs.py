def test_markdown_formatter_sanity(testdir, tmp_path, expected_output):
    path = tmp_path / 'doc.md'
    testdir.copy_example("test_suite.py")
    testdir.runpytest(
        '--docs', '{}'.format(path)
    )
    assert path.read_text() == expected_output('markdown_sanity.md')


def test_rst_formatter_sanity(testdir, tmp_path, expected_output):
    path = tmp_path / 'doc.rst'
    testdir.copy_example("test_suite.py")
    testdir.runpytest(
        '--docs', '{}'.format(path),
        '--doc-type', 'rst'
    )
    assert path.read_text() == expected_output('rst_sanity.rst')
