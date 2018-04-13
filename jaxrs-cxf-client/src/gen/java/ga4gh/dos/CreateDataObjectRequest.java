package ga4gh.dos;

import ga4gh.dos.DataObject;
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
  * The Data Object one would like to index. One must provide any aliases and URLs to this file when sending the CreateDataObjectRequest. It is up to implementations to validate that the Data Object is available from the provided URLs.
 **/
@ApiModel(description="The Data Object one would like to index. One must provide any aliases and URLs to this file when sending the CreateDataObjectRequest. It is up to implementations to validate that the Data Object is available from the provided URLs.")
public class CreateDataObjectRequest  {
  
  @ApiModelProperty(value = "REQUIRED The data object to be created. The ID scheme is left up to the implementor but should be unique to the server instance.")
 /**
   * REQUIRED The data object to be created. The ID scheme is left up to the implementor but should be unique to the server instance.  
  **/
  private DataObject dataObject = null;
 /**
   * REQUIRED The data object to be created. The ID scheme is left up to the implementor but should be unique to the server instance.
   * @return dataObject
  **/
  @JsonProperty("data_object")
  public DataObject getDataObject() {
    return dataObject;
  }

  public void setDataObject(DataObject dataObject) {
    this.dataObject = dataObject;
  }

  public CreateDataObjectRequest dataObject(DataObject dataObject) {
    this.dataObject = dataObject;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class CreateDataObjectRequest {\n");
    
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

