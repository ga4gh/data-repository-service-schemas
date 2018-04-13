
# DataObject

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | REQUIRED An identifier unique to this Data Object. |  [optional]
**name** | **String** | OPTIONAL A string that can be optionally used to name a Data Object. |  [optional]
**size** | **String** | REQUIRED The computed size in bytes. |  [optional]
**created** | [**OffsetDateTime**](OffsetDateTime.md) | REQUIRED Timestamp of object creation in RFC3339. |  [optional]
**updated** | [**OffsetDateTime**](OffsetDateTime.md) | OPTIONAL Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates. |  [optional]
**version** | **String** | OPTIONAL A string representing a version. |  [optional]
**mimeType** | **String** | OPTIONAL A string providing the mime-type of the Data Object. For example, \&quot;application/json\&quot;. |  [optional]
**checksums** | [**List&lt;Checksum&gt;**](Checksum.md) | REQUIRED The checksum of the Data Object. At least one checksum must be provided. |  [optional]
**urls** | [**List&lt;URL&gt;**](URL.md) | OPTIONAL The list of URLs that can be used to access the Data Object. |  [optional]
**description** | **String** | OPTIONAL A human readable description of the contents of the Data Object. |  [optional]
**aliases** | **List&lt;String&gt;** | OPTIONAL A list of strings that can be used to find this Data Object. These aliases can be used to represent the Data Object&#39;s location in a directory (e.g. \&quot;bucket/folder/file.name\&quot;) to make Data Objects more discoverable. They might also be used to represent |  [optional]



