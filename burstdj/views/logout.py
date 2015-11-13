from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.view import view_config


class LogoutViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)