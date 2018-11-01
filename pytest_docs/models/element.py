from ..plugin import PYTEST_DOC_MARKER
from ..pytest_utils.utils import unique_identifier, element_name, element_markers, element_desc, format_markers


class Element:
    def __init__(self, element: 'Element' = None, type_: str = None):
        self.raw_element = element
        self.type_ = type_
        self.unique_id = None
        self.raw_name = None
        self.raw_markers = []
        self.desc = None
        self.parent = None
        self.children = []
        self.init()

    @classmethod
    def create_doc_tree(cls, items) -> 'Element':
        tree = cls()
        for item in items:
            tree.add(cls(item.module)).add(cls(item.cls)).add(cls(item))
        return tree

    def add(self, element: 'Element') -> 'Element':
        if element not in self.children:
            element.parent = self
            self.children.append(element)
        return self.children[self.children.index(element)]

    def init(self):
        if self.raw_element:
            self.unique_id = unique_identifier(self.raw_element)
            self.raw_name = element_name(self.raw_element)
            self.raw_markers = element_markers(self.raw_element)
            self.desc = element_desc(self.raw_element)

    @property
    def markers(self) -> list:
        return format_markers(self.raw_markers)

    @property
    def name(self) -> str:
        for marker in self.raw_markers:
            if marker.name == PYTEST_DOC_MARKER:
                return marker.kwargs['name']
        return self.raw_name

    def __repr__(self):
        return f'<Element(name={self.name}>'

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.unique_id)

    def __eq__(self, other):
        if not isinstance(other, Element):
            raise TypeError
        return self.unique_id == other.unique_id
