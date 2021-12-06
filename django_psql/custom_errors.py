class APIException(Exception):

    def __init__(self, message, status=None):
        self.context = {}
        if status:
            self.context['status'] = status
        super().__init__(message)