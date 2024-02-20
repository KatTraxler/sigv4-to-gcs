# Sigv4 to GCS XML API


## Description

A simple python script that creates signed headers for authenticating to the GCS XML APIs

## Getting Started

### Dependencies

- Python 3
- Curl


### Required command-line arguements

* --access_key: The ID of the HMAC key used to authenticate to GCS XML API 
* --secret_key: The HMAC key secret key used to authenticate to GCS XML API 
* --OBJECT_NAME: The name of the object to upload to the bucket.
* --bucket_name: The name of the GCS bucket to upload the object to.
* --content_type: Type of object (i.e. text/plain or application/json)

### Returned

The output of the script is the curl command to execute which will upload the object to the specified GCS bucket.


## Authors

Contributors names and contact info

ex. Kat Traxler 
ex. [@NightmareJs](https://twitter.com/nightmarejs)


## Acknowledgments

Inspiration, code snippets, etc.
* [Rosy Parmar](https://medium.com/@rosyparmar/google-cloud-storage-use-hmac-to-authenticate-requests-to-cloud-storage-aa8ed859be33)