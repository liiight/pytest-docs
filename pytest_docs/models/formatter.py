from itertools import chain

from .element import Element


class Formatter:
    name = None

    @staticmethod
    def _default_format(element) -> str:
        return element

    module_name_format = _default_format
    module_desc_format = _default_format
    class_name_format = _default_format
    class_desc_format = _default_format
    func_name_format = _default_format
    func_desc_format = _default_format
    marker_format = _default_format
    marker_prefix = "Markers"

    def create_document(self, doc_tree: Element) -> str:
        out = []
        for module in doc_tree.children:
            out += self._doc_element(module, self.module_name_format, self.module_desc_format)
            for class_ in module.children:
                out += self._doc_element(class_, self.class_name_format, self.class_desc_format)
                for func in class_.children:
                    out += self._doc_element(func, self.func_name_format, self.func_desc_format)
        return ''.join(out)

    def _element_markers(self, element: Element) -> list:
        marker_doc = []
        if element.markers:
            marker_doc.append(self.marker_prefix)
            for marker in element.markers:
                marker_doc.append(self.marker_format(marker))
        return marker_doc

    def _doc_element(self, element, element_name_fmt, element_desc_fmt) -> list:
        element_doc = [element_name_fmt(element.name)]
        if element.desc:
            element_doc.append(element_desc_fmt(element.desc))
        element_doc += self._element_markers(element)
        element_doc = self._add_new_lines(element_doc)
        return element_doc

    @staticmethod
    def _add_new_lines(element_doc: list) -> list:
        return list(chain.from_iterable(zip(element_doc, ['\n' for _ in element_doc])))
