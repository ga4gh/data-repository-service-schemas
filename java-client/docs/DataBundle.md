
# DataBundle

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | REQUIRED An identifier, unique to this Data Bundle |  [optional]
**dataObjectIds** | **List&lt;String&gt;** | REQUIRED The list of Data Objects that this Data Bundle contains. |  [optional]
**created** | [**OffsetDateTime**](OffsetDateTime.md) | REQUIRED Timestamp of object creation in RFC3339. |  [optional]
**updated** | [**OffsetDateTime**](OffsetDateTime.md) | REQUIRED Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates. |  [optional]
**version** | **String** | REQUIRED A string representing a version, some systems may use checksum, a RFC3339 timestamp, or incrementing version number. For systems that do not support versioning please use your update timestamp as your version. |  [optional]
**checksums** | [**List&lt;Checksum&gt;**](Checksum.md) | REQUIRED At least one checksum must be provided. The data bundle checksum is computed over all the checksums of the Data Objects that bundle contains. |  [optional]
**description** | **String** | OPTIONAL A human readable description. |  [optional]
**aliases** | **List&lt;String&gt;** | OPTIONAL A list of strings that can be used to identify this Data Bundle. |  [optional]
**systemMetadata** | [**SystemMetadata**](SystemMetadata.md) |  |  [optional]
**userMetadata** | [**UserMetadata**](UserMetadata.md) |  |  [optional]



