import ssl
import socket
from datetime import datetime


def get_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as conn:
            with context.wrap_socket(conn, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        if not cert:
            return {"status": "Invalid", "issuer": "N/A", "expiration": "N/A"}
        issuer = cert.get("issuer", [])
        issuer_dict = {
        }
        for item in issuer:
            key, value = item[0]
            issuer_dict[key] = value

        cert_details = {
            "issuer": issuer_dict,
            "expiration": cert.get("notAfter", ""),
            "status": "Valid" if cert else "Invalid"
        }
        expiration_date = cert_details["expiration"]
        expiration_date = datetime.strptime(expiration_date, "%b %d %H:%M:%S %Y GMT").strftime('%Y-%m-%d %H:%M:%S')

        cert_details["expiration"] = expiration_date

        return cert_details
    except ssl.SSLError as e:
        return {"status": "Invalid", "issuer": "N/A", "expiration": "N/A"}
    except socket.error as e:
        return {"status": "Invalid", "issuer": "N/A", "expiration": "N/A"}
    except Exception as e:
        return {"status": "Invalid", "issuer": "N/A", "expiration": "N/A"}



domain = "facebook.com"
certificate_info = get_ssl_certificate(domain)

print(f"SSL Certificate Information for {domain}:")
print(f"Status: {certificate_info['status']}")
print(f"Issuer: {certificate_info['issuer']}")
print(f"Expiration Date: {certificate_info['expiration']}")
