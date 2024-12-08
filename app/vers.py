from flask import Blueprint, session
import multiprocessing, logging
from app.loggingSystem import setup_logger

def userError():
    return session.get("username", None) is not None


processorscount = multiprocessing.cpu_count()
processors = max(1, processorscount // 4)
outputDir="output_json"
domainsjsonfile="_domains.json"
usersjsonfile = 'users.json'
secret_key = 'your_secret_key'
setting = 'config.settings'
NUM=0
sessiontimeout = 10
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
thread = None
app = None
DomainsList = []
UsersList = []
logger = setup_logger("logs/flask_app.log", logging.DEBUG)
auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)
domain_bp = Blueprint('domain', __name__)
main_bp = Blueprint('main', __name__)
