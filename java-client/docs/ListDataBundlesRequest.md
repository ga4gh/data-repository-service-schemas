
# ListDataBundlesRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **String** | OPTIONAL If provided returns Data Bundles that have any alias that matches the request. |  [optional]
**checksum** | [**Checksum**](Checksum.md) | OPTIONAL If provided, will only return Data Bundles which have the provided checksum. |  [optional]
**pageSize** | **Integer** | OPTIONAL Specifies the maximum number of results to return in a single page. If unspecified, a system default will be used. |  [optional]
**pageToken** | **String** | OPTIONAL The continuation token, which is used to page through large result sets. To get the next page of results, set this parameter to the value of &#x60;next_page_token&#x60; from the previous response. |  [optional]



