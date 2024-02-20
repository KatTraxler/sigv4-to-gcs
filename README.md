# Sigv4 to GCS XML API


## Description

A simple python script that creates signed headers for authenticating to the GCS XML APIs. It takes in an access key, secret, object and bucket name and returns a curl request with a signed Authorization header which will retreive the GCS object.

## Getting Started

### Dependencies

- Python 3
- Curl

### Requirements

* Caller must have the `storage.objects.get` permission on the requested object.
* Caller must supply an [HMAC key](https://cloud.google.com/storage/docs/authentication/hmackeys)


### Required command-line arguements

* --access_key: The ID of the HMAC key used to authenticate to GCS XML API .
* --secret_key: The HMAC key secret key used to authenticate to GCS XML API. 
* --OBJECT_NAME: The name of the object to retreive from the GCS bucket.
* --bucket_name: The name of the GCS bucket to retreive the object from.

### Returned

The output of the script is the curl command to execute which will upload the object to the specified GCS bucket.


## Authors

Contributors names and contact info

ex. Kat Traxler 
ex. [@NightmareJs](https://twitter.com/nightmarejs)


## Acknowledgments

Inspiration, code snippets, etc.
* [Rosy Parmar](https://medium.com/@rosyparmar/google-cloud-storage-use-hmac-to-authenticate-requests-to-cloud-storage-aa8ed859be33)