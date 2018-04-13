package ga4gh.dos;

import ga4gh.dos.Checksum;
import ga4gh.dos.SystemMetadata;
import ga4gh.dos.UserMetadata;
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

public class DataBundle  {
  
  @ApiModelProperty(value = "REQUIRED An identifier, unique to this Data Bundle")
 /**
   * REQUIRED An identifier, unique to this Data Bundle  
  **/
  private String id = null;

  @ApiModelProperty(value = "REQUIRED The list of Data Objects that this Data Bundle contains.")
 /**
   * REQUIRED The list of Data Objects that this Data Bundle contains.  
  **/
  private List<String> dataObjectIds = null;

  @ApiModelProperty(value = "REQUIRED Timestamp of object creation in RFC3339.")
 /**
   * REQUIRED Timestamp of object creation in RFC3339.  
  **/
  private Date created = null;

  @ApiModelProperty(value = "REQUIRED Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates.")
 /**
   * REQUIRED Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates.  
  **/
  private Date updated = null;

  @ApiModelProperty(value = "REQUIRED A string representing a version, some systems may use checksum, a RFC3339 timestamp, or incrementing version number. For systems that do not support versioning please use your update timestamp as your version.")
 /**
   * REQUIRED A string representing a version, some systems may use checksum, a RFC3339 timestamp, or incrementing version number. For systems that do not support versioning please use your update timestamp as your version.  
  **/
  private String version = null;

  @ApiModelProperty(value = "REQUIRED At least one checksum must be provided. The data bundle checksum is computed over all the checksums of the Data Objects that bundle contains.")
 /**
   * REQUIRED At least one checksum must be provided. The data bundle checksum is computed over all the checksums of the Data Objects that bundle contains.  
  **/
  private List<Checksum> checksums = null;

  @ApiModelProperty(value = "OPTIONAL A human readable description.")
 /**
   * OPTIONAL A human readable description.  
  **/
  private String description = null;

  @ApiModelProperty(value = "OPTIONAL A list of strings that can be used to identify this Data Bundle.")
 /**
   * OPTIONAL A list of strings that can be used to identify this Data Bundle.  
  **/
  private List<String> aliases = null;

  @ApiModelProperty(value = "")
  private SystemMetadata systemMetadata = null;

  @ApiModelProperty(value = "")
  private UserMetadata userMetadata = null;
 /**
   * REQUIRED An identifier, unique to this Data Bundle
   * @return id
  **/
  @JsonProperty("id")
  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public DataBundle id(String id) {
    this.id = id;
    return this;
  }

 /**
   * REQUIRED The list of Data Objects that this Data Bundle contains.
   * @return dataObjectIds
  **/
  @JsonProperty("data_object_ids")
  public List<String> getDataObjectIds() {
    return dataObjectIds;
  }

  public void setDataObjectIds(List<String> dataObjectIds) {
    this.dataObjectIds = dataObjectIds;
  }

  public DataBundle dataObjectIds(List<String> dataObjectIds) {
    this.dataObjectIds = dataObjectIds;
    return this;
  }

  public DataBundle addDataObjectIdsItem(String dataObjectIdsItem) {
    this.dataObjectIds.add(dataObjectIdsItem);
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

  public DataBundle created(Date created) {
    this.created = created;
    return this;
  }

 /**
   * REQUIRED Timestamp of update in RFC3339, identical to create timestamp in systems that do not support updates.
   * @return updated
  **/
  @JsonProperty("updated")
  public Date getUpdated() {
    return updated;
  }

  public void setUpdated(Date updated) {
    this.updated = updated;
  }

  public DataBundle updated(Date updated) {
    this.updated = updated;
    return this;
  }

 /**
   * REQUIRED A string representing a version, some systems may use checksum, a RFC3339 timestamp, or incrementing version number. For systems that do not support versioning please use your update timestamp as your version.
   * @return version
  **/
  @JsonProperty("version")
  public String getVersion() {
    return version;
  }

  public void setVersion(String version) {
    this.version = version;
  }

  public DataBundle version(String version) {
    this.version = version;
    return this;
  }

 /**
   * REQUIRED At least one checksum must be provided. The data bundle checksum is computed over all the checksums of the Data Objects that bundle contains.
   * @return checksums
  **/
  @JsonProperty("checksums")
  public List<Checksum> getChecksums() {
    return checksums;
  }

  public void setChecksums(List<Checksum> checksums) {
    this.checksums = checksums;
  }

  public DataBundle checksums(List<Checksum> checksums) {
    this.checksums = checksums;
    return this;
  }

  public DataBundle addChecksumsItem(Checksum checksumsItem) {
    this.checksums.add(checksumsItem);
    return this;
  }

 /**
   * OPTIONAL A human readable description.
   * @return description
  **/
  @JsonProperty("description")
  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public DataBundle description(String description) {
    this.description = description;
    return this;
  }

 /**
   * OPTIONAL A list of strings that can be used to identify this Data Bundle.
   * @return aliases
  **/
  @JsonProperty("aliases")
  public List<String> getAliases() {
    return aliases;
  }

  public void setAliases(List<String> aliases) {
    this.aliases = aliases;
  }

  public DataBundle aliases(List<String> aliases) {
    this.aliases = aliases;
    return this;
  }

  public DataBundle addAliasesItem(String aliasesItem) {
    this.aliases.add(aliasesItem);
    return this;
  }

 /**
   * Get systemMetadata
   * @return systemMetadata
  **/
  @JsonProperty("system_metadata")
  public SystemMetadata getSystemMetadata() {
    return systemMetadata;
  }

  public void setSystemMetadata(SystemMetadata systemMetadata) {
    this.systemMetadata = systemMetadata;
  }

  public DataBundle systemMetadata(SystemMetadata systemMetadata) {
    this.systemMetadata = systemMetadata;
    return this;
  }

 /**
   * Get userMetadata
   * @return userMetadata
  **/
  @JsonProperty("user_metadata")
  public UserMetadata getUserMetadata() {
    return userMetadata;
  }

  public void setUserMetadata(UserMetadata userMetadata) {
    this.userMetadata = userMetadata;
  }

  public DataBundle userMetadata(UserMetadata userMetadata) {
    this.userMetadata = userMetadata;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class DataBundle {\n");
    
    sb.append("    id: ").append(toIndentedString(id)).append("\n");
    sb.append("    dataObjectIds: ").append(toIndentedString(dataObjectIds)).append("\n");
    sb.append("    created: ").append(toIndentedString(created)).append("\n");
    sb.append("    updated: ").append(toIndentedString(updated)).append("\n");
    sb.append("    version: ").append(toIndentedString(version)).append("\n");
    sb.append("    checksums: ").append(toIndentedString(checksums)).append("\n");
    sb.append("    description: ").append(toIndentedString(description)).append("\n");
    sb.append("    aliases: ").append(toIndentedString(aliases)).append("\n");
    sb.append("    systemMetadata: ").append(toIndentedString(systemMetadata)).append("\n");
    sb.append("    userMetadata: ").append(toIndentedString(userMetadata)).append("\n");
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

