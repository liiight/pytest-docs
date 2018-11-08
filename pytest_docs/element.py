import inspect
from enum import Enum

from _pytest.mark.structures import MarkDecorator
from pytest import Function

from .utils import methdispatch

PYTEST_DOC_MARKER = "pytest_doc"


class ElementType(Enum):
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    NONE = None


class Element:
    """Represent the document consistent of the separate elements.
     A recursive tree structure where each element can have a parent, siblings or children.
      A module is a parent of a class, class of a function."""

    def __init__(self, element: "Element" = None):
        self.raw_element = element
        self.raw_markers = self.element_markers(element)
        self.type_ = self.element_type(element) if element else ElementType.NONE
        self.unique_id = self.unique_identifier(element)
        self.raw_name = self.element_name(element)
        self.desc = self.element_desc(element)

        self.parent = None
        self.children = []

    def __iter__(self):
        return iter(self.children)

    @property
    def top(self):
        return self.parent is None

    @property
    def siblings(self):
        """Return a generator of :class:`Element` that share the same parent as current element"""
        return (elem for elem in self.parent if elem is not self) if self.parent else ()

    @methdispatch
    def element_type(self, element) -> ElementType:
        return (
            ElementType.CLASS
            if hasattr(element, "__qualname__")
            else ElementType.MODULE
        )

    @element_type.register(Function)
    def _(self, element) -> ElementType:
        return ElementType.FUNCTION

    @classmethod
    def create_doc_tree(cls, items) -> "Element":
        tree = cls()
        for item in items:
            tree.add(cls(item.module)).add(cls(item.cls)).add(cls(item))
        return tree

    @methdispatch
    def element_name(self, element) -> str:
        return element.__name__ if element else ""

    @element_name.register(Function)
    def _(self, element) -> str:
        return element.originalname or element.name

    @methdispatch
    def element_desc(self, element) -> str:
        return element.__doc__ if element else ""

    @element_desc.register(Function)
    def _(self, element) -> str:
        return element.function.__doc__

    @methdispatch
    def format_marker(self, marker_data):
        data = ["(", ")"]
        data.insert(1, "".join(["{}".format(arg) for arg in marker_data]))
        return "".join(data)

    @format_marker.register(dict)
    def _(self, marker_data):
        data = ["(", ")"]
        data.insert(
            1,
            "".join(["{}={}".format(key, value) for key, value in marker_data.items()]),
        )
        return "".join(data)

    def marker_details(self, marker):
        args = kwargs = ""
        if marker.args:
            args = self.format_marker(marker.args)

        if marker.kwargs:
            kwargs = self.format_marker(marker.kwargs)

        out = [marker.name, args, kwargs]
        return " ".join(out).strip()

    @methdispatch
    def get_marker(self, marker):
        return self.marker_details(marker)

    @get_marker.register(MarkDecorator)
    def _(self, marker):
        return self.marker_details(marker.mark)

    def add(self, element: "Element") -> "Element":
        if element not in self.children:
            element.parent = self
            self.children.append(element)
        return self.children[self.children.index(element)]

    def format_markers(self, markers):
        return [self.get_marker(marker) for marker in markers]

    @methdispatch
    def element_markers(self, element):
        markers = getattr(element, "pytestmark", [])
        if not isinstance(markers, list):
            markers = [markers]
        return markers

    @element_markers.register(Function)
    def _(self, element):
        return element.own_markers

    @methdispatch
    def unique_identifier(self, element):
        if not element:
            return None
        qualname = getattr(element, "__qualname__", None)
        source_file = inspect.getsourcefile(element)
        if qualname:
            return "{}/{}".format(source_file, qualname)
        return source_file

    @unique_identifier.register(Function)
    def _(self, element):
        return element.nodeid

    @property
    def markers(self) -> list:
        return self.format_markers(self.raw_markers)

    @property
    def name(self) -> str:
        for marker in self.raw_markers:
            if marker.name == PYTEST_DOC_MARKER:
                return marker.kwargs["name"]
        return self.raw_name

    def __repr__(self):
        return "<Element(name={}>".format(self.name)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.unique_id)

    def __eq__(self, other):
        if not isinstance(other, Element):
            raise TypeError
        return self.unique_id == other.unique_id
