from pathlib import Path

from .element import Element
from .formatters.markdown import MarkdownFormatter
from .formatters.restuctured import RSTFormatter

FORMATTERS = {
    MarkdownFormatter.name: MarkdownFormatter(),
    RSTFormatter.name: RSTFormatter(),
}


class DocPlugin:
    def __init__(self, config):
        self.config = config
        self.path = config.getvalue("docs_path")
        self.format_type = config.getvalue("docs_type")

    def pytest_runtestloop(self, session):
        if not self.path:
            return

        doc_tree = Element.create_doc_tree(session.items)

        fmt = FORMATTERS[self.format_type]
        out = fmt.create_document(doc_tree)

        path = Path(self.path)
        path.write_text(out)

    def pytest_terminal_summary(self, terminalreporter, exitstatus):
        if self.path:
            terminalreporter.write_sep("-", "generated doc file: {}".format(self.path))


def pytest_addoption(parser):
    group = parser.getgroup("docs generator")
    group.addoption("--docs", dest="docs_path", help="create documentation given path")
    group.addoption(
        "--doc-type",
        dest="docs_type",
        default="md",
        help="Choose document type",
        choices=list(FORMATTERS),
    )


def pytest_configure(config):
    docs = DocPlugin(config)
    config.pluginmanager.register(docs, "pytest-docs")
