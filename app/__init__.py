from flask import Flask
from app.controllers import auth_controller, domain_controller, main_contoller, api_controller
import datetime, logging
from app.vers import *
from app.models import threads, handlers
from flask_wtf.csrf import CSRFProtect


def create_app():
    global csrf, NUM
    handlers.checkdir()
    threads.startThread(3600)
    app = Flask(__name__)
    app.config.from_object(setting)
    app.secret_key = secret_key
    csrf = CSRFProtect(app)
    app.permanent_session_lifetime = datetime.timedelta(hours=sessiontimeout)
    app.register_blueprint(main_contoller.main_bp)
    app.register_blueprint(api_controller.api_bp)
    app.register_blueprint(auth_controller.auth_bp)
    app.register_blueprint(domain_controller.domain_bp)
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    if NUM == 0:
        NUM += 0
        logger.info("Hassan DevOps Application Project Initialized Successfully.")
    return app
