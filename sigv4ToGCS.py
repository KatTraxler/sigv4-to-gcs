import hmac
import hashlib
import base64
import datetime
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--access_key",
    help="The id of the HMAC Key",
    required=True,
    type=str,
    dest="access_key",
)
parser.add_argument(
    "--secret_key",
    help="The secret value of the HMAC Key",
    required=True,
    type=str,
    dest="secret_key",
)
parser.add_argument(
    "--OBJECT_NAME",
    help="Name of the GCS object to retrieve",
    required=True,
    type=str,
    dest="OBJECT_NAME",
)
parser.add_argument(
    "--bucket_name",
    help="Name of the bucket to retreive an object from",
    required=True,
    type=str,
    dest="bucket_name",
)


args = parser.parse_args()

## Credit: https://medium.com/@rosyparmar/google-cloud-storage-use-hmac-to-authenticate-requests-to-cloud-storage-aa8ed859be33

algorithm = 'GOOG4-HMAC-SHA256'
BUCKET_NAME = args.bucket_name
OBJECT_NAME = args.OBJECT_NAME
method = 'GET'

query_string = 'uploads='
host = f'{BUCKET_NAME}.storage.googleapis.com'

access_key = args.access_key
secret_key = args.secret_key
content_type = "text/plain"
content_length = 0
x_goog_expires = 604800

# Fetch current time to form credential scope
t = datetime.datetime.utcnow()
google_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')

# Location of GCS Bucket
region = 'us-central1'

# Service name. When accessing Cloud Storage resources, this value is storage
service = 'storage'

# When accessing Cloud Storage resources, this value is goog4_request
request_type = 'goog4_request'

credential_scope = date_stamp + '/' + region + '/' + service + '/' + request_type

signed_headers = 'content-length;content-type;host;x-goog-content-sha256;x-goog-date;x-goog-expires'


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    key_date = sign(('GOOG4' + key).encode('utf-8'), date_stamp)
    key_region = sign(key_date, regionName)
    key_service = sign(key_region, serviceName)
    signing_key = sign(key_service, 'goog4_request')
    return signing_key


# Construct the canonical request as a string.Canonical requests define the elements of a request that a user must include 
canonical_uri = f'/{OBJECT_NAME}'
canonical_headers = 'content-length:' + str(content_length) + '\n' + 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-goog-content-sha256:UNSIGNED-PAYLOAD' + '\n' + 'x-goog-date:' + google_date + '\n' + 'x-goog-expires:' + str(x_goog_expires)
canonical_request = method + '\n' + canonical_uri + '\n' + query_string + '\n' + canonical_headers + '\n\n' + signed_headers + '\n' + 'UNSIGNED-PAYLOAD'

# Construct string-to-sign.
string_to_sign = algorithm + '\n' +  google_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

# Derive the signing key from the HMAC key
signing_key = getSignatureKey(secret_key, date_stamp, region, service)

# Sign the string-to-sign using an RSA signature with SHA-256
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature


##############################################
## Test the returned authorization header with curl by attempting to Post an object to the GCS bucket:
##############################################

print("\nRun the following curl command to verify you can upload an object to the provided GCS bucket:")

print("curl -v -X GET -H 'Content-Type: " + content_type + "' -H 'Content-length: " + str(content_length) + "' -H 'x-goog-date: " + google_date + "' -H 'x-goog-expires: " + str(x_goog_expires) + "' -H 'x-goog-content-sha256: UNSIGNED-PAYLOAD' -H 'Authorization: " + authorization_header + "' https://" + host + canonical_uri + "?" + query_string)


