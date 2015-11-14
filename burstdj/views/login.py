from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.view import view_config

from burstdj.logic import security
from burstdj.logic.security import USERS


class LoginViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='login', renderer='../templates/login.pt')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        username = ''
        password = ''

        if request.method == 'POST':
            username = request.params.get('username', None)
            headers = None

            if username:
                headers = security.authenticate_user(request, username)
            if headers:
                return HTTPFound(
                    location='/room',
                    headers=headers,
                )

            message = 'Failed login'

        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            username=username,
            password=password,
        )
