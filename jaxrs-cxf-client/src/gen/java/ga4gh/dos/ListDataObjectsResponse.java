package ga4gh.dos;

import ga4gh.dos.DataObject;
import io.swagger.annotations.ApiModel;
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

/**
  * A list of Data Objects matching the requested parameters, and a paging token, that can be used to retrieve more results.
 **/
@ApiModel(description="A list of Data Objects matching the requested parameters, and a paging token, that can be used to retrieve more results.")
public class ListDataObjectsResponse  {
  
  @ApiModelProperty(value = "The list of Data Objects.")
 /**
   * The list of Data Objects.  
  **/
  private List<DataObject> dataObjects = null;

  @ApiModelProperty(value = "The continuation token, which is used to page through large result sets. Provide this value in a subsequent request to return the next page of results. This field will be empty if there aren't any additional results.")
 /**
   * The continuation token, which is used to page through large result sets. Provide this value in a subsequent request to return the next page of results. This field will be empty if there aren't any additional results.  
  **/
  private String nextPageToken = null;
 /**
   * The list of Data Objects.
   * @return dataObjects
  **/
  @JsonProperty("data_objects")
  public List<DataObject> getDataObjects() {
    return dataObjects;
  }

  public void setDataObjects(List<DataObject> dataObjects) {
    this.dataObjects = dataObjects;
  }

  public ListDataObjectsResponse dataObjects(List<DataObject> dataObjects) {
    this.dataObjects = dataObjects;
    return this;
  }

  public ListDataObjectsResponse addDataObjectsItem(DataObject dataObjectsItem) {
    this.dataObjects.add(dataObjectsItem);
    return this;
  }

 /**
   * The continuation token, which is used to page through large result sets. Provide this value in a subsequent request to return the next page of results. This field will be empty if there aren&#39;t any additional results.
   * @return nextPageToken
  **/
  @JsonProperty("next_page_token")
  public String getNextPageToken() {
    return nextPageToken;
  }

  public void setNextPageToken(String nextPageToken) {
    this.nextPageToken = nextPageToken;
  }

  public ListDataObjectsResponse nextPageToken(String nextPageToken) {
    this.nextPageToken = nextPageToken;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ListDataObjectsResponse {\n");
    
    sb.append("    dataObjects: ").append(toIndentedString(dataObjects)).append("\n");
    sb.append("    nextPageToken: ").append(toIndentedString(nextPageToken)).append("\n");
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

