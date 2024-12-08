import re
import requests
import ssl
import socket
from datetime import datetime
from app.vers import *
from app.models import handlers


def URLstatus(domain):
    resp = requests.get(f"https://{domain}", headers=header)
    return "Live" if resp.status_code == 200 else "Down"


def get_ssl_certificate(domain, status, username):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as conn:
            with context.wrap_socket(conn, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        if not cert:
            return False, {"status": status, "ssl_issuer": "N/A", "ssl_expiration": "N/A"}
        issuer = cert.get("issuer", [])
        cert_details = {
            "ssl_issuer": "",
            "ssl_expiration": "",
            "status": status
        }
        for item in issuer:
            key, value = item[0]
            if key == "organizationName":
                cert_details["ssl_issuer"] = value
        expiration_date = datetime.strptime(cert.get("notAfter", ""), "%b %d %H:%M:%S %Y GMT").strftime('%Y-%m-%d')
        cert_details["ssl_expiration"] = expiration_date
        logger.info(f"Add the {domain} domain at the user {username}: {cert_details}")
        return True, cert_details
    except (ssl.SSLError, socket.error, Exception) as e:
        logger.error(f"Error: {e}")
        return False, {"status": status, "ssl_issuer": "N/A", "ssl_expiration": "N/A"}


def createDomainDict(domain, username):
    status = "Down"
    status = URLstatus(domain)
    if status == "Down":
        return {"status": status, "ssl_issuer": "N/A", "ssl_expiration": "N/A"}
    _, cert_details = get_ssl_certificate(domain, status, username)
    return cert_details


def validate_domain(domain):
    if domain.startswith("http://"):
        domain= domain.replace("http://", "")
    elif domain.startswith("https://"):
        domain = domain.replace("https://", "")
    pattern = r"^(?!-)(?:[A-Za-z0-9-]{1,120}(?=\.[A-Za-z0-9-]{2,})(?:\.[A-Za-z]{2,}){1,3})$"
    if re.match(pattern, domain):
        return True
    else:
        return False


def add_domain(domain, username):
    if domain == "":
        msg = "Can't use empty domain"
        logger.error(msg)
        return False, msg
    elif username == "":
        msg = "Can't use empty username"
        logger.error(msg)
        return False, msg
    elif not validate_domain(domain):
        msg = "Invalid domain format"
        logger.error(msg)
        return False, msg
    _, domains = handlers.checkFile(f"{outputDir}/{username}{domainsjsonfile}")
    if domain in [domain['domain'] for domain in domains]:
        msg = "Domain was found in the user domains"
        logger.error(msg)
        return False, msg
    domains.append({**{"domain": domain}, **createDomainDict(domain, username)})
    status = handlers.dumpJson(f"{outputDir}/{username}{domainsjsonfile}",domains)
    msg = "Domain added successfully"
    logger.info(msg)
    return True, msg


def bulk_upload_domains(file,username):
    userSuccess = []
    for line in file:
        status, _ = add_domain(line, username)
        if status:
            userSuccess.append(line)
    if len(userSuccess) == 0:
        msg = "Invalid file format or content"
        logger.error(msg)
        return False, msg
    msg = "Bulk upload successful"
    logger.info(msg)
    return True, msg
