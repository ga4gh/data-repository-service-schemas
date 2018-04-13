# DataObjectServiceApi

All URIs are relative to *http://localhost/ga4gh/dos/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createDataBundle**](DataObjectServiceApi.md#createDataBundle) | **POST** /databundles | Create a new Data Bundle
[**createDataObject**](DataObjectServiceApi.md#createDataObject) | **POST** /dataobjects | Make a new Data Object
[**deleteDataBundle**](DataObjectServiceApi.md#deleteDataBundle) | **DELETE** /databundles/{data_bundle_id} | Delete a Data Bundle
[**deleteDataObject**](DataObjectServiceApi.md#deleteDataObject) | **DELETE** /dataobjects/{data_object_id} | Delete a Data Object index entry
[**getDataBundle**](DataObjectServiceApi.md#getDataBundle) | **GET** /databundles/{data_bundle_id} | Retrieve a Data Bundle
[**getDataBundleVersions**](DataObjectServiceApi.md#getDataBundleVersions) | **GET** /databundles/{data_bundle_id}/versions | Retrieve all versions of a Data Bundle
[**getDataObject**](DataObjectServiceApi.md#getDataObject) | **GET** /dataobjects/{data_object_id} | Retrieve a Data Object
[**getDataObjectVersions**](DataObjectServiceApi.md#getDataObjectVersions) | **GET** /dataobjects/{data_object_id}/versions | Retrieve all versions of a Data Object
[**listDataBundles**](DataObjectServiceApi.md#listDataBundles) | **POST** /databundles/list | List the Data Bundles
[**listDataObjects**](DataObjectServiceApi.md#listDataObjects) | **POST** /dataobjects/list | List the Data Objects
[**updateDataBundle**](DataObjectServiceApi.md#updateDataBundle) | **PUT** /databundles/{data_bundle_id} | Update a Data Bundle
[**updateDataObject**](DataObjectServiceApi.md#updateDataObject) | **PUT** /dataobjects/{data_object_id} | Update a Data Object


<a name="createDataBundle"></a>
# **createDataBundle**
> CreateDataBundleResponse createDataBundle(body)

Create a new Data Bundle

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
CreateDataBundleRequest body = new CreateDataBundleRequest(); // CreateDataBundleRequest | 
try {
    CreateDataBundleResponse result = apiInstance.createDataBundle(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#createDataBundle");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateDataBundleRequest**](CreateDataBundleRequest.md)|  |

### Return type

[**CreateDataBundleResponse**](CreateDataBundleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createDataObject"></a>
# **createDataObject**
> CreateDataObjectResponse createDataObject(body)

Make a new Data Object

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
CreateDataObjectRequest body = new CreateDataObjectRequest(); // CreateDataObjectRequest | 
try {
    CreateDataObjectResponse result = apiInstance.createDataObject(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#createDataObject");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateDataObjectRequest**](CreateDataObjectRequest.md)|  |

### Return type

[**CreateDataObjectResponse**](CreateDataObjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteDataBundle"></a>
# **deleteDataBundle**
> DeleteDataBundleResponse deleteDataBundle(dataBundleId)

Delete a Data Bundle

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataBundleId = "dataBundleId_example"; // String | 
try {
    DeleteDataBundleResponse result = apiInstance.deleteDataBundle(dataBundleId);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#deleteDataBundle");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataBundleId** | **String**|  |

### Return type

[**DeleteDataBundleResponse**](DeleteDataBundleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteDataObject"></a>
# **deleteDataObject**
> DeleteDataObjectResponse deleteDataObject(dataObjectId)

Delete a Data Object index entry

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataObjectId = "dataObjectId_example"; // String | 
try {
    DeleteDataObjectResponse result = apiInstance.deleteDataObject(dataObjectId);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#deleteDataObject");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataObjectId** | **String**|  |

### Return type

[**DeleteDataObjectResponse**](DeleteDataObjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getDataBundle"></a>
# **getDataBundle**
> GetDataBundleResponse getDataBundle(dataBundleId, version)

Retrieve a Data Bundle

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataBundleId = "dataBundleId_example"; // String | 
String version = "version_example"; // String | OPTIONAL If provided will return the requested version of the selected Data Bundle. Otherwise, only the latest version is returned.
try {
    GetDataBundleResponse result = apiInstance.getDataBundle(dataBundleId, version);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#getDataBundle");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataBundleId** | **String**|  |
 **version** | **String**| OPTIONAL If provided will return the requested version of the selected Data Bundle. Otherwise, only the latest version is returned. | [optional]

### Return type

[**GetDataBundleResponse**](GetDataBundleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getDataBundleVersions"></a>
# **getDataBundleVersions**
> GetDataBundleVersionsResponse getDataBundleVersions(dataBundleId)

Retrieve all versions of a Data Bundle

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataBundleId = "dataBundleId_example"; // String | 
try {
    GetDataBundleVersionsResponse result = apiInstance.getDataBundleVersions(dataBundleId);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#getDataBundleVersions");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataBundleId** | **String**|  |

### Return type

[**GetDataBundleVersionsResponse**](GetDataBundleVersionsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getDataObject"></a>
# **getDataObject**
> GetDataObjectResponse getDataObject(dataObjectId, version)

Retrieve a Data Object

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataObjectId = "dataObjectId_example"; // String | 
String version = "version_example"; // String | OPTIONAL If provided will return the requested version of the selected Data Object.
try {
    GetDataObjectResponse result = apiInstance.getDataObject(dataObjectId, version);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#getDataObject");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataObjectId** | **String**|  |
 **version** | **String**| OPTIONAL If provided will return the requested version of the selected Data Object. | [optional]

### Return type

[**GetDataObjectResponse**](GetDataObjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getDataObjectVersions"></a>
# **getDataObjectVersions**
> GetDataObjectVersionsResponse getDataObjectVersions(dataObjectId)

Retrieve all versions of a Data Object

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataObjectId = "dataObjectId_example"; // String | 
try {
    GetDataObjectVersionsResponse result = apiInstance.getDataObjectVersions(dataObjectId);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#getDataObjectVersions");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataObjectId** | **String**|  |

### Return type

[**GetDataObjectVersionsResponse**](GetDataObjectVersionsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listDataBundles"></a>
# **listDataBundles**
> ListDataBundlesResponse listDataBundles(body)

List the Data Bundles

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
ListDataBundlesRequest body = new ListDataBundlesRequest(); // ListDataBundlesRequest | 
try {
    ListDataBundlesResponse result = apiInstance.listDataBundles(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#listDataBundles");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ListDataBundlesRequest**](ListDataBundlesRequest.md)|  |

### Return type

[**ListDataBundlesResponse**](ListDataBundlesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listDataObjects"></a>
# **listDataObjects**
> ListDataObjectsResponse listDataObjects(body)

List the Data Objects

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
ListDataObjectsRequest body = new ListDataObjectsRequest(); // ListDataObjectsRequest | 
try {
    ListDataObjectsResponse result = apiInstance.listDataObjects(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#listDataObjects");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ListDataObjectsRequest**](ListDataObjectsRequest.md)|  |

### Return type

[**ListDataObjectsResponse**](ListDataObjectsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateDataBundle"></a>
# **updateDataBundle**
> UpdateDataBundleResponse updateDataBundle(dataBundleId, body)

Update a Data Bundle

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataBundleId = "dataBundleId_example"; // String | 
UpdateDataBundleRequest body = new UpdateDataBundleRequest(); // UpdateDataBundleRequest | 
try {
    UpdateDataBundleResponse result = apiInstance.updateDataBundle(dataBundleId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#updateDataBundle");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataBundleId** | **String**|  |
 **body** | [**UpdateDataBundleRequest**](UpdateDataBundleRequest.md)|  |

### Return type

[**UpdateDataBundleResponse**](UpdateDataBundleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateDataObject"></a>
# **updateDataObject**
> UpdateDataObjectResponse updateDataObject(dataObjectId, body)

Update a Data Object

### Example
```java
// Import classes:
//import invalidPackageName.ApiException;
//import ga4gh.DataObjectServiceApi;


DataObjectServiceApi apiInstance = new DataObjectServiceApi();
String dataObjectId = "dataObjectId_example"; // String | 
UpdateDataObjectRequest body = new UpdateDataObjectRequest(); // UpdateDataObjectRequest | 
try {
    UpdateDataObjectResponse result = apiInstance.updateDataObject(dataObjectId, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DataObjectServiceApi#updateDataObject");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataObjectId** | **String**|  |
 **body** | [**UpdateDataObjectRequest**](UpdateDataObjectRequest.md)|  |

### Return type

[**UpdateDataObjectResponse**](UpdateDataObjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

