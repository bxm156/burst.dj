from pyramid import httpexceptions
from pyramid.response import Response
import simplejson as json



def json_error_helper(self):
    body = {'status': self.status, 'title': self.title}
    Response.__init__(self, json.dumps(body))
    self.content_type = 'application/json'


class HTTPBadRequest(httpexceptions.HTTPBadRequest):
    def __init__(self):
        super(HTTPBadRequest, self).__init__()
        json_error_helper(self)


class HTTPConflict(httpexceptions.HTTPConflict):
    def __init__(self):
        super(HTTPConflict, self).__init__()
        json_error_helper(self)


class HTTPNotFound(httpexceptions.HTTPNotFound):
    def __init__(self):
        super(HTTPNotFound, self).__init__()
        json_error_helper(self)


class HTTPForbidden(httpexceptions.HTTPForbidden):
    def __init__(self):
        super(HTTPForbidden, self).__init__()
        json_error_helper(self)
