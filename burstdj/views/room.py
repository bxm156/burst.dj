from pyramid.view import view_config


@view_config(route_name='room_page', renderer='../templates/room.pt')
def room(request):
    return {}
