from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from burstdj.logic import security
from burstdj.models import DBSession
from burstdj.models.mymodel import MyModel


@view_config(route_name='home', renderer='../templates/index.pt')
def home(request):
    # try:
    #     one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(conn_err_msg, content_type='text/plain', status_int=500)

    if not security.is_request_authenticated(request):
        return HTTPFound(
            location='/login'
        )
    else:
        return HTTPFound(
            location='/room'
        )

    # return {'one': one, 'project': 'burst.dj'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_burst.dj_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

