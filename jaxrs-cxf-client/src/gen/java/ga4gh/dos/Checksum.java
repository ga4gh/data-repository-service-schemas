package ga4gh.dos;


import io.swagger.annotations.ApiModelProperty;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Checksum  {
  
  @ApiModelProperty(value = "REQUIRED The hex-string encoded checksum for the Data.")
 /**
   * REQUIRED The hex-string encoded checksum for the Data.  
  **/
  private String checksum = null;

  @ApiModelProperty(value = "OPTIONAL The digest method used to create the checksum. If left unspecified md5 will be assumed.  possible values: md5                # most blob stores provide a checksum using this multipart-md5      # multipart uploads provide a specialized tag in S3 sha256 sha512")
 /**
   * OPTIONAL The digest method used to create the checksum. If left unspecified md5 will be assumed.  possible values: md5                # most blob stores provide a checksum using this multipart-md5      # multipart uploads provide a specialized tag in S3 sha256 sha512  
  **/
  private String type = null;
 /**
   * REQUIRED The hex-string encoded checksum for the Data.
   * @return checksum
  **/
  @JsonProperty("checksum")
  public String getChecksum() {
    return checksum;
  }

  public void setChecksum(String checksum) {
    this.checksum = checksum;
  }

  public Checksum checksum(String checksum) {
    this.checksum = checksum;
    return this;
  }

 /**
   * OPTIONAL The digest method used to create the checksum. If left unspecified md5 will be assumed.  possible values: md5                # most blob stores provide a checksum using this multipart-md5      # multipart uploads provide a specialized tag in S3 sha256 sha512
   * @return type
  **/
  @JsonProperty("type")
  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public Checksum type(String type) {
    this.type = type;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class Checksum {\n");
    
    sb.append("    checksum: ").append(toIndentedString(checksum)).append("\n");
    sb.append("    type: ").append(toIndentedString(type)).append("\n");
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

