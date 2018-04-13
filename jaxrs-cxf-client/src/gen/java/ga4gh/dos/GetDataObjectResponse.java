package ga4gh.dos;

import ga4gh.dos.DataObject;

import io.swagger.annotations.ApiModelProperty;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import com.fasterxml.jackson.annotation.JsonProperty;

public class GetDataObjectResponse  {
  
  @ApiModelProperty(value = "REQUIRED The Data Object that coincides with a specific GetDataObjectRequest.")
 /**
   * REQUIRED The Data Object that coincides with a specific GetDataObjectRequest.  
  **/
  private DataObject dataObject = null;
 /**
   * REQUIRED The Data Object that coincides with a specific GetDataObjectRequest.
   * @return dataObject
  **/
  @JsonProperty("data_object")
  public DataObject getDataObject() {
    return dataObject;
  }

  public void setDataObject(DataObject dataObject) {
    this.dataObject = dataObject;
  }

  public GetDataObjectResponse dataObject(DataObject dataObject) {
    this.dataObject = dataObject;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class GetDataObjectResponse {\n");
    
    sb.append("    dataObject: ").append(toIndentedString(dataObject)).append("\n");
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

