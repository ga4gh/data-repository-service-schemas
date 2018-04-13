
# ListDataObjectsRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **String** | OPTIONAL If provided will only return Data Objects with the given alias. |  [optional]
**url** | **String** | OPTIONAL If provided will return only Data Objects with a that URL matches this string. |  [optional]
**checksum** | [**ChecksumRequest**](ChecksumRequest.md) | OPTIONAL If provided will only return data object messages with the provided checksum. If the checksum type is provided |  [optional]
**pageSize** | **Integer** | OPTIONAL Specifies the maximum number of results to return in a single page. If unspecified, a system default will be used. |  [optional]
**pageToken** | **String** | OPTIONAL The continuation token, which is used to page through large result sets. To get the next page of results, set this parameter to the value of &#x60;next_page_token&#x60; from the previous response. |  [optional]



