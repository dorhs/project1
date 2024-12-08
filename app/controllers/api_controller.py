import json, hashlib, os
from app.vers import *
from app.models import handlers
from app.services import auth_service, domain_service
from flask import request, session, jsonify


@api_bp.route('/api/login', methods=['POST'])
def login():
    _, users = handlers.checkFile(usersjsonfile)
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    except Exception as e:
        dic = {"status": "Error", "message": f"Invalid JSON payload: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 400
    status, message = auth_service.login_user(username=username, password=password)
    if status:
        session['username'] = username
        dic = {"status": "Success", "message": message}
        logger.info(f"{dic}")
        return jsonify(dic), 200
    else:
        dic = {"status": "Error", "message": message}
        logger.error(f"{dic}")
        return jsonify(dic), 400

@api_bp.route('/api/register', methods=['POST'])
def register():
    _, users = handlers.checkFile(usersjsonfile)
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    except Exception as e:
        dic ={"status": "Error", "message": f"Invalid JSON payload: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 400
    status, message = auth_service.register_user(username=username, password=password)
    if status:
        dic= {"status": "Success", "message": message}
        logger.info(f"{dic}")
        return jsonify(dic), 200
    else:
        dic = {"status": "Error", "message": message}
        logger.error(f"{dic}")
        return jsonify(dic), 400


@api_bp.route('/api/add_domain', methods=['POST'])
def addDomain():
    stat = userError()
    if not stat:
        dic = {"status": "Error", "message": "User not logged in"}
        logger.error(f"{dic}")
        return jsonify(dic), 401
    try:
        data = request.get_json()
        domain = data.get("domain")
    except Exception as e:
        dic = {"status": "Error", "message": f"Invalid JSON payload: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 400
    username = session.get('username', None)
    if username is None:
        dic = {"status": "Error", "message": "The username session is empty"}
        logger.error(f"{dic}")
        return jsonify(dic), 401
    status, message = domain_service.add_domain(domain=domain, username=username)
    if status:
        dic = {"status": "Success", "message": message}
        logger.info(f"{dic}")
        return jsonify(dic), 200
    else:
        dic = {"status": "Error", "message": message}
        logger.error(f"{dic}")
        return jsonify(dic), 400




@api_bp.route('/api/bulk_upload', methods=['POST'])
def addBulk():
    stat = userError()
    if not stat:
        dic = {"status": "Error", "message": "User not logged in"}
        logger.error(f"{dic}")
        return jsonify(dic), 401
    try:
        data = request.get_json()
        path = data.get("filepath")
    except Exception as e:
        dic = {"status": "Error", "message": f"Invalid JSON payload: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 400
    try:
        with open(path, "r") as f:
            text = f.read().split("\n")
    except (FileNotFoundError,PermissionError, IsADirectoryError) as e:
        logger.error(f"File Error: {e}")
        text = []
    username = session.get('username', None)
    status, message = domain_service.bulk_upload_domains(file=text, username=username)
    if status:
        dic = {"status": "Success", "message": message}
        logger.info(f"{dic}")
        return jsonify(dic), 200
    else:
        dic = {"status": "Error", "message": message}
        logger.error(f"{dic}")
        return jsonify(dic), 400


@api_bp.route('/api/update', methods=['POST'])
def update_domain():
    data = request.json
    username = session.get('username', None)
    if not username:
        dic = {"error": True, "message": "User not logged in"}
        logger.error(f"{dic}")
        return jsonify(dic), 401
    domain = data.get('domain')
    if not domain:
        dic = {"error": True, "message": "Domain not provided"}
        logger.error(f"{dic}")
        return jsonify(dic), 400
    dictdomain = {"domain": domain, **domain_service.createDomainDict(domain, username)}
    file_path = f"{outputDir}/{username}{domainsjsonfile}"
    try:
        with open(file_path, "r+") as f:
            try:
                text = json.load(f)
            except json.JSONDecodeError:
                text = []
            updated = False
            for index, item in enumerate(text):
                if item["domain"] == domain:
                    text[index] = dictdomain
                    updated = True
                    break
            if not updated:
                text.append(dictdomain)
            f.seek(0)
            f.truncate()
            json.dump(text, f, indent=4)
    except FileNotFoundError as e:
        dic = {"error": True, "message": f"File not found: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 404
    except Exception as e:
        dic = {"error": True, "message": f"Internal server error: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 500
    dic = {"success": True, "updated_domain": dictdomain}
    logger.info(f"{dic}")
    return jsonify(dic), 200


@api_bp.route('/api/delete', methods=['POST'])
def delete_domain():
    data = request.json
    username = session.get('username', None)
    if not username:
        dic = {"error": True, "message": "User not logged in"}
        logger.error(f"{dic}")
        return jsonify(dic), 401
    domain = data.get('domain')
    if not domain:
        dic = {"error": True, "message": "Domain not provided"}
        logger.error(f"{dic}")
        return jsonify(dic), 400
    file_path = f"{outputDir}/{username}{domainsjsonfile}"
    try:
        with open(file_path, "r+") as f:
            try:
                text = json.load(f)
            except json.JSONDecodeError:
                text = []
            updated = False
            for index, item in enumerate(text):
                if item["domain"] == domain:
                    text.pop(index)
                    updated = True
                    break
            if not updated:
                return jsonify({"error": True, "message": "Domain not found"}), 404
            f.seek(0)
            f.truncate()
            json.dump(text, f, indent=4)
    except FileNotFoundError as e:
        dic = {"error": True, "message": f"File not found: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 404
    except Exception as e:
        dic = {"error": True, "message": f"Internal server error: {e}"}
        logger.error(f"{dic}")
        return jsonify(dic), 500
    dic = {"message": f"Domain {domain} deleted successfully"}
    logger.info(f"{dic}")
    return jsonify(dic), 200

