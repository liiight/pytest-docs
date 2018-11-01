from ..models.formatter import Formatter


class MarkdownFormatter(Formatter):
    name = 'md'
    marker_prefix = "\n**Markers:**"

    @staticmethod
    def module_name_format(element):
        return '# {}'.format(element)

    @staticmethod
    def class_name_format(element):
        return '## {}'.format(element)

    @staticmethod
    def func_name_format(element):
        return '### {}'.format(element)

    @staticmethod
    def marker_format(marker):
        return "- {}".format(marker)
