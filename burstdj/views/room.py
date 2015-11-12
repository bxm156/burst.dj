from pyramid.view import view_config


@view_config(route_name='room', renderer='../templates/room.pt')
def room(request):
    return {}
