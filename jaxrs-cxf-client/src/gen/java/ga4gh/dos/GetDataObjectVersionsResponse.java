package ga4gh.dos;

import ga4gh.dos.DataObject;
import java.util.ArrayList;
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

public class GetDataObjectVersionsResponse  {
  
  @ApiModelProperty(value = "REQUIRED All versions of the Data Objects that match the GetDataObjectVersions request.")
 /**
   * REQUIRED All versions of the Data Objects that match the GetDataObjectVersions request.  
  **/
  private List<DataObject> dataObjects = null;
 /**
   * REQUIRED All versions of the Data Objects that match the GetDataObjectVersions request.
   * @return dataObjects
  **/
  @JsonProperty("data_objects")
  public List<DataObject> getDataObjects() {
    return dataObjects;
  }

  public void setDataObjects(List<DataObject> dataObjects) {
    this.dataObjects = dataObjects;
  }

  public GetDataObjectVersionsResponse dataObjects(List<DataObject> dataObjects) {
    this.dataObjects = dataObjects;
    return this;
  }

  public GetDataObjectVersionsResponse addDataObjectsItem(DataObject dataObjectsItem) {
    this.dataObjects.add(dataObjectsItem);
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class GetDataObjectVersionsResponse {\n");
    
    sb.append("    dataObjects: ").append(toIndentedString(dataObjects)).append("\n");
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

