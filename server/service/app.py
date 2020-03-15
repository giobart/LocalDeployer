from flask import Flask
from service.api import blueprints
from service.tasks.startup_app import time_loop
from service.config import LOGGER_LEVEL


__all__ = ('create_app',)


def create_app(config=None, app_name='service'):
    '''
    Prepares initializes the application and its utilities.
    '''

    app = Flask(app_name)
    app.logger.setLevel(LOGGER_LEVEL)

    if config:
        app.config.from_pyfile(config)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    time_loop.start(block=False)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=20002)
