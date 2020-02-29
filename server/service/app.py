from flask import Flask
from server.service.api import blueprints


__all__ = ('create_app',)

def create_app(config=None, app_name='service'):
    '''
    Prepares initializes the application and its utilities.
    '''

    app = Flask(app_name)

    if config:
        app.config.from_pyfile(config)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=20002)
