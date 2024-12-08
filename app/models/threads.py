import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from app.services.domain_service import URLstatus, get_ssl_certificate
from app.models.handlers import loadJson, dumpJson
from app.vers import *

processed_files = set()

def process_domain(domain, user):
    """
    Process a single domain: check status and SSL certificate details.
    """
    status = URLstatus(domain['domain'])
    if status == "Down":
        msg = {"domain": domain['domain'], "status": status, "ssl_issuer": "N/A", "ssl_expiration": "N/A"}
        logger.error(str(msg))
        return msg
    else:
        _, cert_details = get_ssl_certificate(domain['domain'], status, user)
        msg = {"domain": domain['domain'], **cert_details}
        logger.info(str(msg))
        return msg


def process_file(file):
    """
    Process a single JSON file: load domains, process them, and save the results.
    """
    status, domains = loadJson(file)
    if not status:
        return
    with ThreadPoolExecutor(max_workers=processors) as executor:
        user = file.replace(domainsjsonfile,"").replace(f"{outputDir}/", "")
        finaldomains = list(executor.map(process_domain, domains, user))
    dumpJson(file, finaldomains)


def updateThread(timeout):
    """
    Continuously check the status of domains listed in JSON files
    and update the results in parallel using a thread pool.
    """
    global processed_files
    while True:
        files = [f"{outputDir}/{file}" for file in os.listdir(outputDir) if domainsjsonfile in file and file not in processed_files]
        print(files)
        with ThreadPoolExecutor(max_workers=processors) as executor:
            executor.map(process_file, files)
        processed_files.update(files)
        time.sleep(timeout)
        processed_files.clear()
        logger.info("Thread update the values of domains for all users.")


def startThread(timeout):
    global thread
    thread = threading.Thread(target=updateThread, args=(timeout,), daemon=True)
    thread.start()


def stopThread():
    global thread
    if thread is not None:
        thread.join()
        thread = None


def restartThread(timeout):
    stopThread()
    startThread(timeout)
