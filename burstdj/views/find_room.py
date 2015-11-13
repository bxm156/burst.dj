from pyramid.view import view_config


@view_config(route_name='find_room', renderer='../templates/find_room.pt')
def room(request):
    return {}
