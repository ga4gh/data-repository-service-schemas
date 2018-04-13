package ga4gh.dos;

import io.swagger.annotations.ApiModel;

import io.swagger.annotations.ApiModelProperty;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import com.fasterxml.jackson.annotation.JsonProperty;

/**
  * An object that can optionally include information about the error.
 **/
@ApiModel(description="An object that can optionally include information about the error.")
public class ErrorResponse  {
  
  @ApiModelProperty(value = "A detailed error message.")
 /**
   * A detailed error message.  
  **/
  private String msg = null;

  @ApiModelProperty(value = "The integer representing the HTTP status code (e.g. 200, 404).")
 /**
   * The integer representing the HTTP status code (e.g. 200, 404).  
  **/
  private Integer statusCode = null;
 /**
   * A detailed error message.
   * @return msg
  **/
  @JsonProperty("msg")
  public String getMsg() {
    return msg;
  }

  public void setMsg(String msg) {
    this.msg = msg;
  }

  public ErrorResponse msg(String msg) {
    this.msg = msg;
    return this;
  }

 /**
   * The integer representing the HTTP status code (e.g. 200, 404).
   * @return statusCode
  **/
  @JsonProperty("status_code")
  public Integer getStatusCode() {
    return statusCode;
  }

  public void setStatusCode(Integer statusCode) {
    this.statusCode = statusCode;
  }

  public ErrorResponse statusCode(Integer statusCode) {
    this.statusCode = statusCode;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ErrorResponse {\n");
    
    sb.append("    msg: ").append(toIndentedString(msg)).append("\n");
    sb.append("    statusCode: ").append(toIndentedString(statusCode)).append("\n");
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

