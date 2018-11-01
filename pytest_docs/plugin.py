from pathlib import Path

from .formatters import markdown, restuctured
from .models.element import Element

PYTEST_DOC_MARKER = 'pytest_doc'

FORMATTERS = {
    markdown.MarkdownFormatter.name: markdown.MarkdownFormatter,
    restuctured.RSTFormatter.name: restuctured.RSTFormatter
}


class DocPlugin:

    def __init__(self, config):
        self.config = config
        self.path = config.getvalue('docs_path')
        self.format_type = config.getvalue('docs_type')

    def pytest_runtestloop(self, session):
        if not self.path:
            return

        doc_tree = Element.create_doc_tree(session.items)

        fmt = FORMATTERS[self.format_type](doc_tree)
        out = fmt.create_document()

        path = Path(self.path)
        path.write_text(out)

    def pytest_terminal_summary(self, terminalreporter, exitstatus):
        if self.path:
            terminalreporter.write_sep('-', 'generated doc file: {}'.format(self.path))
