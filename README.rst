===========
pytest-docs
===========

A `pytest`_ plugin that generates documentation of the testing application itself.

.. image:: https://img.shields.io/pypi/v/pytest-docs.svg
    :target: https://pypi.org/project/pytest-docs
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-docs.svg
    :target: https://pypi.org/project/pytest-docs
    :alt: Python versions

.. image:: https://travis-ci.org/liiight/pytest_docs.svg?branch=master
    :target: https://travis-ci.org/liiight/pytest-docs
    :alt: Travis CI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Black

.. image:: https://pepy.tech/badge/pytest-docs
    :target: https://pepy.tech/project/pytest-docs
    :alt: Pepy.tech


Features
--------

Create documentation of your tests. Turns this:

.. code-block::

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

To this:

.. code-block::

    # Test Docs
    This is the module doc

    **Markers:**
    - module_mark
    - module_mark_2
    - pytest_doc  (name=Test Docs)
    ## Test Class
    This is the class doc

    **Markers:**
    - pytest_doc  (name=Test Class)
    - class_marker
    ### test_func_a
    This is the doc for test_func_a

    **Markers:**
    - func_mark_a (foo)
    ### test_func_b
    This is the doc for test_func_b

    **Markers:**
    - kwarg_mark  (goo=bla)

Current supported formats:

- Markdown
- reStrcutured text

Why not sphinx?
---------------

(More accurately, why not sphinx-autodoc?)
Sphinx is an amazing tool that I use and used in other project. To use its autodoc plugin, it need the documented plugin to be importable by the python interperter. Pytest test collection and invocation uses a completely separate mechanism.
If you believe that it somehow possible to use sphinx to create pytest documentation, please do not hesitate to contact me.

Requirements
------------

- Python 3.4, 3.5, 3.6 or 3.7
- Pytest >= 3.5.0

Installation
------------

You can install "pytest-docs" via `pip`_ from `PyPI`_::

    $ pip install pytest-docs


Usage
-----

Use ``--docs [PATH]`` to create the documentation.

Use ``--doc-type`` to select the type (currently supports ``md`` and ``rst``)

Use  ``@pytest.mark.pytest_doc(name="Test Class")`` to override name of element. It'll override name based on the place it is being used (module, class or function).

**Note:** pytest-docs uses the pytest collection mechanism, so your documentation will be generated according the the usual collection commands used to run the tests.

What's planned ahead
--------------------

1. See if anyone is even interested in this
2. Document fixtures
3. Document tests and fixtures parametrization
4. Custom formatters via hooks

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-docs" is free and open source software

Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/liiight/pytest-docs/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.
