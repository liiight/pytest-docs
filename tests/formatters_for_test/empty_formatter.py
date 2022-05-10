from pytest_docs.formatter import Formatter



class CustomFormatter(Formatter):
    name = "md"
    marker_prefix = ""

    @staticmethod
    def module_name_format(element):
        return ""
    @staticmethod
    def class_name_format(element):
        return ""

    @staticmethod
    def func_name_format(element):
        return ""

    @staticmethod
    def marker_format(marker):
        return ""
