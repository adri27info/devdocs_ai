from rest_framework.parsers import MultiPartParser, JSONParser


class MultiPartParserMixin:
    """
    Mixin to set MultiPartParser as the parser class for a view.
    """
    parser_classes = [MultiPartParser]


class JSONParserMixin:
    """
    Mixin to set JSONParser as the parser class for a view.
    """
    parser_classes = [JSONParser]


class FlexibleParserMixin:
    """
    Mixin to provide flexible parsers based on request method.

    Returns JSONParser by default and both JSONParser + MultiPartParser for
    POST, PUT, PATCH requests.
    """
    def get_parser_classes(self):
        if hasattr(self, 'request') and self.request is not None:
            if self.request.method in ['POST', 'PUT', 'PATCH']:
                return [JSONParser, MultiPartParser]
        return [JSONParser]
