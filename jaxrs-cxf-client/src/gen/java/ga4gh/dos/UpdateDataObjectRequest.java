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

public class UpdateDataObjectRequest  {
  
  @ApiModelProperty(value = "REQUIRED The identifier of the Data Object to be updated.")
 /**
   * REQUIRED The identifier of the Data Object to be updated.  
  **/
  private String dataObjectId = null;

  @ApiModelProperty(value = "REQUIRED The new Data Object for this identifier.")
 /**
   * REQUIRED The new Data Object for this identifier.  
  **/
  private DataObject dataObject = null;
 /**
   * REQUIRED The identifier of the Data Object to be updated.
   * @return dataObjectId
  **/
  @JsonProperty("data_object_id")
  public String getDataObjectId() {
    return dataObjectId;
  }

  public void setDataObjectId(String dataObjectId) {
    this.dataObjectId = dataObjectId;
  }

  public UpdateDataObjectRequest dataObjectId(String dataObjectId) {
    this.dataObjectId = dataObjectId;
    return this;
  }

 /**
   * REQUIRED The new Data Object for this identifier.
   * @return dataObject
  **/
  @JsonProperty("data_object")
  public DataObject getDataObject() {
    return dataObject;
  }

  public void setDataObject(DataObject dataObject) {
    this.dataObject = dataObject;
  }

  public UpdateDataObjectRequest dataObject(DataObject dataObject) {
    this.dataObject = dataObject;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class UpdateDataObjectRequest {\n");
    
    sb.append("    dataObjectId: ").append(toIndentedString(dataObjectId)).append("\n");
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

