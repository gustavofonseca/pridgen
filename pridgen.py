from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid import httpexceptions

import base28

DEFAULT_CHAR_COUNT = 10

@view_config(route_name='home', renderer='pridgen:home.pt')
def generate(request):

    try:
        char_count = int(request.params.get('char_count', DEFAULT_CHAR_COUNT))
    except ValueError:
        char_count = DEFAULT_CHAR_COUNT

    try:
        pseudo_random_id = base28.genbase(char_count)
    except:
        raise httpexceptions.HTTPBadRequest()

    return {'generated_id': pseudo_random_id,
            'default_char_count': DEFAULT_CHAR_COUNT,
            'char_count': char_count}

if __name__ == '__main__':
    config = Configurator()
    config.add_route('home', '/')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()