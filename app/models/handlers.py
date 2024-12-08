import json, os
from flask import session
from app.vers import *


def userError():
    username = session.get('username')
    if not username:
        return False
    else:
        return True


def loadJson(jsonfile):
    if os.path.exists(jsonfile):
        try:
            with open(jsonfile, "r") as f:
                text = json.load(f)
                return True, text
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"File Error: {e}")
            return False, []
    else:
        return False, []


def checkdir():
    if not os.path.exists(outputDir):
        logger.error(f"Creating an directory: {outputDir}")
        os.mkdir(outputDir)
    checkFile(usersjsonfile)

def checkFile(jsonfile):
    path = f"{os.getcwd()}/{jsonfile}"
    if not os.path.exists(path):
        return dumpJson(path, []), []
    else:
        status, values = loadJson(path)
        return status, values


def dumpJson(jsonfile, info):
    try:
        with open(jsonfile, "w") as f:
            json.dump(info, f, indent=4)
            return True
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"File Error: {e}")
        return False


