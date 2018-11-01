import inspect
from functools import singledispatch

from _pytest.mark.structures import MarkDecorator
from pytest import Function


@singledispatch
def element_name(element):
    return element.__name__


@element_name.register(Function)
def _(element):
    return element.originalname or element.name


@singledispatch
def element_desc(element):
    return element.__doc__


@element_desc.register(Function)
def _(element):
    return element.function.__doc__


@singledispatch
def format_marker(marker_data):
    data = ['(', ')']
    data.insert(1, ''.join(['{}'.format(arg) for arg in marker_data]))
    return ''.join(data)


@format_marker.register(dict)
def _(marker_data):
    data = ['(', ')']
    data.insert(1, ''.join(['{}={}'.format(key, value) for key, value in marker_data.items()]))
    return ''.join(data)


def marker_details(marker):
    args = kwargs = ''
    if marker.args:
        args = format_marker(marker.args)

    if marker.kwargs:
        kwargs = format_marker(marker.kwargs)

    out = [
        marker.name,
        args,
        kwargs
    ]
    return ' '.join(out)


@singledispatch
def get_marker(marker):
    return marker_details(marker)


@get_marker.register(MarkDecorator)
def _(marker):
    return marker_details(marker.mark)


def format_markers(markers):
    return [get_marker(marker) for marker in markers]


@singledispatch
def element_markers(element):
    markers = getattr(element, 'pytestmark', [])
    if not isinstance(markers, list):
        markers = [markers]
    return markers


@element_markers.register(Function)
def _(element):
    return element.own_markers


@singledispatch
def unique_identifier(element):
    qualname = getattr(element, '__qualname__', None)
    source_file = inspect.getsourcefile(element)
    if qualname:
        return f'{source_file}/{qualname}'
    return source_file


@unique_identifier.register(Function)
def _(element):
    return element.nodeid
