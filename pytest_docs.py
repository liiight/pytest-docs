# -*- coding: utf-8 -*-
from pytest_docs import plugin


def pytest_addoption(parser):
    group = parser.getgroup('docs generator')
    group.addoption(
        '--docs',
        dest='docs_path',
        help='create documentation given path'
    )
    group.addoption(
        '--doc-type',
        dest='docs_type',
        default='md',
        help='Choose document type',
        choices=list(plugin.FORMATTERS)
    )


def pytest_configure(config):
    docs = plugin.DocPlugin(config)
    config.pluginmanager.register(docs, docs)
