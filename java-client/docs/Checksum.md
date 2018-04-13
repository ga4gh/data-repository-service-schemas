
# Checksum

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum** | **String** | REQUIRED The hex-string encoded checksum for the Data. |  [optional]
**type** | **String** | OPTIONAL The digest method used to create the checksum. If left unspecified md5 will be assumed.  possible values: md5                # most blob stores provide a checksum using this multipart-md5      # multipart uploads provide a specialized tag in S3 sha256 sha512 |  [optional]



