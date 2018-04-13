
# ChecksumRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum** | **String** | REQUIRED The hexlified checksum that one would like to match on. |  [optional]
**type** | **String** | OPTIONAL If provided will restrict responses to those that match the provided type.  possible values: md5                # most blob stores provide a checksum using this multipart-md5      # multipart uploads provide a specialized tag in S3 sha256 sha512 |  [optional]



