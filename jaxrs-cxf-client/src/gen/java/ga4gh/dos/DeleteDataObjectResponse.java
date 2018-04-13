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

public class DeleteDataObjectResponse  {
  
  @ApiModelProperty(value = "REQUIRED The identifier of the Data Object deleted.")
 /**
   * REQUIRED The identifier of the Data Object deleted.  
  **/
  private String dataObjectId = null;
 /**
   * REQUIRED The identifier of the Data Object deleted.
   * @return dataObjectId
  **/
  @JsonProperty("data_object_id")
  public String getDataObjectId() {
    return dataObjectId;
  }

  public void setDataObjectId(String dataObjectId) {
    this.dataObjectId = dataObjectId;
  }

  public DeleteDataObjectResponse dataObjectId(String dataObjectId) {
    this.dataObjectId = dataObjectId;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class DeleteDataObjectResponse {\n");
    
    sb.append("    dataObjectId: ").append(toIndentedString(dataObjectId)).append("\n");
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

