from argparse import ArgumentError
from pathlib import Path

from .element import Element
from .formatters.markdown import MarkdownFormatter
from .formatters.restuctured import RSTFormatter


formatters = {
    MarkdownFormatter.name: MarkdownFormatter(),
    RSTFormatter.name: RSTFormatter(),
    "custom": "Not implemented",
}


class DocPlugin:
    def __init__(self, path, format_type):
        self.path = path
        self.format_type = format_type

    def pytest_runtestloop(self, session):
        doc_tree = Element.create_doc_tree(session.items)

        fmt = formatters[self.format_type]
        out = fmt.create_document(doc_tree)

        with Path(self.path).open("w", encoding="utf-8") as file:
            file.write(out)

    def pytest_terminal_summary(self, terminalreporter, exitstatus):
        terminalreporter.write_sep("-", "generated doc file: {}".format(self.path))


def pytest_addoption(parser):
    group = parser.getgroup("docs generator")
    group.addoption("--docs", dest="docs_path", help="create documentation given path")
    group.addoption(
        "--doc-type",
        dest="docs_type",
        default="md",
        help="Choose document type",
        choices=list(formatters),
    )
    group.addoption(
        "--custom-formatter-path",
        dest="custom_formatter_path",
        help="Choose custom formatter path",
    )



def pytest_configure(config):
    path = config.getoption("docs_path")
    if path:
        custom_fmt_path = config.getoption("custom_formatter_path")
        if custom_fmt_path is not None:
            fmt_module = __import__(custom_fmt_path, fromlist=['CustomFormatter'])
            fmt_class = getattr(fmt_module, 'CustomFormatter')
            formatters.update({"custom": fmt_class()}) 

        format_type = config.getoption("docs_type")
        config.pluginmanager.register(DocPlugin(path, format_type), "pytest-docs")
