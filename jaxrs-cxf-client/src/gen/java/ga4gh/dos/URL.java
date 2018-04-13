package ga4gh.dos;

import ga4gh.dos.SystemMetadata;
import ga4gh.dos.UserMetadata;

import io.swagger.annotations.ApiModelProperty;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import com.fasterxml.jackson.annotation.JsonProperty;

public class URL  {
  
  @ApiModelProperty(value = "REQUIRED A URL that can be used to access the file.")
 /**
   * REQUIRED A URL that can be used to access the file.  
  **/
  private String url = null;

  @ApiModelProperty(value = "")
  private SystemMetadata systemMetadata = null;

  @ApiModelProperty(value = "")
  private UserMetadata userMetadata = null;
 /**
   * REQUIRED A URL that can be used to access the file.
   * @return url
  **/
  @JsonProperty("url")
  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public URL url(String url) {
    this.url = url;
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

  public URL systemMetadata(SystemMetadata systemMetadata) {
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

  public URL userMetadata(UserMetadata userMetadata) {
    this.userMetadata = userMetadata;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class URL {\n");
    
    sb.append("    url: ").append(toIndentedString(url)).append("\n");
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

