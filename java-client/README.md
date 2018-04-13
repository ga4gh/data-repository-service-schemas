# swagger-java-client

## Requirements

Building the API client library requires [Maven](https://maven.apache.org/) to be installed.

## Installation

To install the API client library to your local Maven repository, simply execute:

```shell
mvn install
```

To deploy it to a remote Maven repository instead, configure the settings of the repository and execute:

```shell
mvn deploy
```

Refer to the [official documentation](https://maven.apache.org/plugins/maven-deploy-plugin/usage.html) for more information.

### Maven users

Add this dependency to your project's POM:

```xml
<dependency>
    <groupId>io.swagger</groupId>
    <artifactId>swagger-java-client</artifactId>
    <version>1.0.0</version>
    <scope>compile</scope>
</dependency>
```

### Gradle users

Add this dependency to your project's build file:

```groovy
compile "io.swagger:swagger-java-client:1.0.0"
```

### Others

At first generate the JAR by executing:

    mvn package

Then manually install the following JARs:

* target/swagger-java-client-1.0.0.jar
* target/lib/*.jar

## Getting Started

Please follow the [installation](#installation) instruction and execute the following Java code:

```java

import invalidPackageName.*;
import invalidPackageName.auth.*;
import ga4gh.dos.*;
import ga4gh.DataObjectServiceApi;

import java.io.File;
import java.util.*;

public class DataObjectServiceApiExample {

    public static void main(String[] args) {
        
        DataObjectServiceApi apiInstance = new DataObjectServiceApi();
        CreateDataBundleRequest body = new CreateDataBundleRequest(); // CreateDataBundleRequest | 
        try {
            CreateDataBundleResponse result = apiInstance.createDataBundle(body);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling DataObjectServiceApi#createDataBundle");
            e.printStackTrace();
        }
    }
}

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost/ga4gh/dos/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DataObjectServiceApi* | [**createDataBundle**](docs/DataObjectServiceApi.md#createDataBundle) | **POST** /databundles | Create a new Data Bundle
*DataObjectServiceApi* | [**createDataObject**](docs/DataObjectServiceApi.md#createDataObject) | **POST** /dataobjects | Make a new Data Object
*DataObjectServiceApi* | [**deleteDataBundle**](docs/DataObjectServiceApi.md#deleteDataBundle) | **DELETE** /databundles/{data_bundle_id} | Delete a Data Bundle
*DataObjectServiceApi* | [**deleteDataObject**](docs/DataObjectServiceApi.md#deleteDataObject) | **DELETE** /dataobjects/{data_object_id} | Delete a Data Object index entry
*DataObjectServiceApi* | [**getDataBundle**](docs/DataObjectServiceApi.md#getDataBundle) | **GET** /databundles/{data_bundle_id} | Retrieve a Data Bundle
*DataObjectServiceApi* | [**getDataBundleVersions**](docs/DataObjectServiceApi.md#getDataBundleVersions) | **GET** /databundles/{data_bundle_id}/versions | Retrieve all versions of a Data Bundle
*DataObjectServiceApi* | [**getDataObject**](docs/DataObjectServiceApi.md#getDataObject) | **GET** /dataobjects/{data_object_id} | Retrieve a Data Object
*DataObjectServiceApi* | [**getDataObjectVersions**](docs/DataObjectServiceApi.md#getDataObjectVersions) | **GET** /dataobjects/{data_object_id}/versions | Retrieve all versions of a Data Object
*DataObjectServiceApi* | [**listDataBundles**](docs/DataObjectServiceApi.md#listDataBundles) | **POST** /databundles/list | List the Data Bundles
*DataObjectServiceApi* | [**listDataObjects**](docs/DataObjectServiceApi.md#listDataObjects) | **POST** /dataobjects/list | List the Data Objects
*DataObjectServiceApi* | [**updateDataBundle**](docs/DataObjectServiceApi.md#updateDataBundle) | **PUT** /databundles/{data_bundle_id} | Update a Data Bundle
*DataObjectServiceApi* | [**updateDataObject**](docs/DataObjectServiceApi.md#updateDataObject) | **PUT** /dataobjects/{data_object_id} | Update a Data Object


## Documentation for Models

 - [Checksum](docs/Checksum.md)
 - [ChecksumRequest](docs/ChecksumRequest.md)
 - [CreateDataBundleRequest](docs/CreateDataBundleRequest.md)
 - [CreateDataBundleResponse](docs/CreateDataBundleResponse.md)
 - [CreateDataObjectRequest](docs/CreateDataObjectRequest.md)
 - [CreateDataObjectResponse](docs/CreateDataObjectResponse.md)
 - [DataBundle](docs/DataBundle.md)
 - [DataObject](docs/DataObject.md)
 - [DeleteDataBundleResponse](docs/DeleteDataBundleResponse.md)
 - [DeleteDataObjectResponse](docs/DeleteDataObjectResponse.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [GetDataBundleResponse](docs/GetDataBundleResponse.md)
 - [GetDataBundleVersionsResponse](docs/GetDataBundleVersionsResponse.md)
 - [GetDataObjectResponse](docs/GetDataObjectResponse.md)
 - [GetDataObjectVersionsResponse](docs/GetDataObjectVersionsResponse.md)
 - [ListDataBundlesRequest](docs/ListDataBundlesRequest.md)
 - [ListDataBundlesResponse](docs/ListDataBundlesResponse.md)
 - [ListDataObjectsRequest](docs/ListDataObjectsRequest.md)
 - [ListDataObjectsResponse](docs/ListDataObjectsResponse.md)
 - [SystemMetadata](docs/SystemMetadata.md)
 - [URL](docs/URL.md)
 - [UpdateDataBundleRequest](docs/UpdateDataBundleRequest.md)
 - [UpdateDataBundleResponse](docs/UpdateDataBundleResponse.md)
 - [UpdateDataObjectRequest](docs/UpdateDataObjectRequest.md)
 - [UpdateDataObjectResponse](docs/UpdateDataObjectResponse.md)
 - [UserMetadata](docs/UserMetadata.md)


## Documentation for Authorization

All endpoints do not require authorization.
Authentication schemes defined for the API:

## Recommendation

It's recommended to create an instance of `ApiClient` per thread in a multithreaded environment to avoid any potential issues.

## Author



