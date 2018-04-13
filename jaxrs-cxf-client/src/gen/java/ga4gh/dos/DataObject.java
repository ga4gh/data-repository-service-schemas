package ga4gh.dos;

import ga4gh.dos.Checksum;
import ga4gh.dos.URL;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import io.swagger.annotations.ApiModelProperty;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import com.fasterxml.jackson.annotation.JsonProperty;

public class DataObject  {
  
  @ApiModelProperty(value = "REQUIRED An identifier unique to this Data Object.")
 /**
   * REQUIRED An identifier unique to this Data Object.  
  **/
  private String id = null;

  @ApiModelProperty(value = "OPTIONAL A string that can be optionally used to name a Data Object.")
 /**
   * OPTIONAL A string that can be optionally used to name a Data Object.  
  **/
  private String name = null;

  @ApiModelProperty(value = "REQUIRED The computed size in bytes.")
 /**
   * REQUIRED The computed size in bytes.  
  **/
  private String size = null;

  @ApiModelProperty(value = "REQUIRED Timestamp of object creation in RFC3339.")
 /**
   * REQUIRED Timestamp of object creation in RFC3339.  
  **/
  private Date created = null;

  @ApiModelProperty(value = "OPTIONAL Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates.")
 /**
   * OPTIONAL Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates.  
  **/
  private Date updated = null;

  @ApiModelProperty(value = "OPTIONAL A string representing a version.")
 /**
   * OPTIONAL A string representing a version.  
  **/
  private String version = null;

  @ApiModelProperty(value = "OPTIONAL A string providing the mime-type of the Data Object. For example, \"application/json\".")
 /**
   * OPTIONAL A string providing the mime-type of the Data Object. For example, \"application/json\".  
  **/
  private String mimeType = null;

  @ApiModelProperty(value = "REQUIRED The checksum of the Data Object. At least one checksum must be provided.")
 /**
   * REQUIRED The checksum of the Data Object. At least one checksum must be provided.  
  **/
  private List<Checksum> checksums = null;

  @ApiModelProperty(value = "OPTIONAL The list of URLs that can be used to access the Data Object.")
 /**
   * OPTIONAL The list of URLs that can be used to access the Data Object.  
  **/
  private List<URL> urls = null;

  @ApiModelProperty(value = "OPTIONAL A human readable description of the contents of the Data Object.")
 /**
   * OPTIONAL A human readable description of the contents of the Data Object.  
  **/
  private String description = null;

  @ApiModelProperty(value = "OPTIONAL A list of strings that can be used to find this Data Object. These aliases can be used to represent the Data Object's location in a directory (e.g. \"bucket/folder/file.name\") to make Data Objects more discoverable. They might also be used to represent")
 /**
   * OPTIONAL A list of strings that can be used to find this Data Object. These aliases can be used to represent the Data Object's location in a directory (e.g. \"bucket/folder/file.name\") to make Data Objects more discoverable. They might also be used to represent  
  **/
  private List<String> aliases = null;
 /**
   * REQUIRED An identifier unique to this Data Object.
   * @return id
  **/
  @JsonProperty("id")
  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public DataObject id(String id) {
    this.id = id;
    return this;
  }

 /**
   * OPTIONAL A string that can be optionally used to name a Data Object.
   * @return name
  **/
  @JsonProperty("name")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public DataObject name(String name) {
    this.name = name;
    return this;
  }

 /**
   * REQUIRED The computed size in bytes.
   * @return size
  **/
  @JsonProperty("size")
  public String getSize() {
    return size;
  }

  public void setSize(String size) {
    this.size = size;
  }

  public DataObject size(String size) {
    this.size = size;
    return this;
  }

 /**
   * REQUIRED Timestamp of object creation in RFC3339.
   * @return created
  **/
  @JsonProperty("created")
  public Date getCreated() {
    return created;
  }

  public void setCreated(Date created) {
    this.created = created;
  }

  public DataObject created(Date created) {
    this.created = created;
    return this;
  }

 /**
   * OPTIONAL Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates.
   * @return updated
  **/
  @JsonProperty("updated")
  public Date getUpdated() {
    return updated;
  }

  public void setUpdated(Date updated) {
    this.updated = updated;
  }

  public DataObject updated(Date updated) {
    this.updated = updated;
    return this;
  }

 /**
   * OPTIONAL A string representing a version.
   * @return version
  **/
  @JsonProperty("version")
  public String getVersion() {
    return version;
  }

  public void setVersion(String version) {
    this.version = version;
  }

  public DataObject version(String version) {
    this.version = version;
    return this;
  }

 /**
   * OPTIONAL A string providing the mime-type of the Data Object. For example, \&quot;application/json\&quot;.
   * @return mimeType
  **/
  @JsonProperty("mime_type")
  public String getMimeType() {
    return mimeType;
  }

  public void setMimeType(String mimeType) {
    this.mimeType = mimeType;
  }

  public DataObject mimeType(String mimeType) {
    this.mimeType = mimeType;
    return this;
  }

 /**
   * REQUIRED The checksum of the Data Object. At least one checksum must be provided.
   * @return checksums
  **/
  @JsonProperty("checksums")
  public List<Checksum> getChecksums() {
    return checksums;
  }

  public void setChecksums(List<Checksum> checksums) {
    this.checksums = checksums;
  }

  public DataObject checksums(List<Checksum> checksums) {
    this.checksums = checksums;
    return this;
  }

  public DataObject addChecksumsItem(Checksum checksumsItem) {
    this.checksums.add(checksumsItem);
    return this;
  }

 /**
   * OPTIONAL The list of URLs that can be used to access the Data Object.
   * @return urls
  **/
  @JsonProperty("urls")
  public List<URL> getUrls() {
    return urls;
  }

  public void setUrls(List<URL> urls) {
    this.urls = urls;
  }

  public DataObject urls(List<URL> urls) {
    this.urls = urls;
    return this;
  }

  public DataObject addUrlsItem(URL urlsItem) {
    this.urls.add(urlsItem);
    return this;
  }

 /**
   * OPTIONAL A human readable description of the contents of the Data Object.
   * @return description
  **/
  @JsonProperty("description")
  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public DataObject description(String description) {
    this.description = description;
    return this;
  }

 /**
   * OPTIONAL A list of strings that can be used to find this Data Object. These aliases can be used to represent the Data Object&#39;s location in a directory (e.g. \&quot;bucket/folder/file.name\&quot;) to make Data Objects more discoverable. They might also be used to represent
   * @return aliases
  **/
  @JsonProperty("aliases")
  public List<String> getAliases() {
    return aliases;
  }

  public void setAliases(List<String> aliases) {
    this.aliases = aliases;
  }

  public DataObject aliases(List<String> aliases) {
    this.aliases = aliases;
    return this;
  }

  public DataObject addAliasesItem(String aliasesItem) {
    this.aliases.add(aliasesItem);
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class DataObject {\n");
    
    sb.append("    id: ").append(toIndentedString(id)).append("\n");
    sb.append("    name: ").append(toIndentedString(name)).append("\n");
    sb.append("    size: ").append(toIndentedString(size)).append("\n");
    sb.append("    created: ").append(toIndentedString(created)).append("\n");
    sb.append("    updated: ").append(toIndentedString(updated)).append("\n");
    sb.append("    version: ").append(toIndentedString(version)).append("\n");
    sb.append("    mimeType: ").append(toIndentedString(mimeType)).append("\n");
    sb.append("    checksums: ").append(toIndentedString(checksums)).append("\n");
    sb.append("    urls: ").append(toIndentedString(urls)).append("\n");
    sb.append("    description: ").append(toIndentedString(description)).append("\n");
    sb.append("    aliases: ").append(toIndentedString(aliases)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private static String toIndentedString(java.lang.Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }
}

