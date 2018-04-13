package ga4gh.dos;

import ga4gh.dos.DataBundle;
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
  * A list of Data Bundles matching the request parameters and a continuation token that can be used to retrieve more results.
 **/
@ApiModel(description="A list of Data Bundles matching the request parameters and a continuation token that can be used to retrieve more results.")
public class ListDataBundlesResponse  {
  
  @ApiModelProperty(value = "The list of Data Bundles.")
 /**
   * The list of Data Bundles.  
  **/
  private List<DataBundle> dataBundles = null;

  @ApiModelProperty(value = "The continuation token, which is used to page through large result sets. Provide this value in a subsequent request to return the next page of results. This field will be empty if there aren't any additional results.")
 /**
   * The continuation token, which is used to page through large result sets. Provide this value in a subsequent request to return the next page of results. This field will be empty if there aren't any additional results.  
  **/
  private String nextPageToken = null;
 /**
   * The list of Data Bundles.
   * @return dataBundles
  **/
  @JsonProperty("data_bundles")
  public List<DataBundle> getDataBundles() {
    return dataBundles;
  }

  public void setDataBundles(List<DataBundle> dataBundles) {
    this.dataBundles = dataBundles;
  }

  public ListDataBundlesResponse dataBundles(List<DataBundle> dataBundles) {
    this.dataBundles = dataBundles;
    return this;
  }

  public ListDataBundlesResponse addDataBundlesItem(DataBundle dataBundlesItem) {
    this.dataBundles.add(dataBundlesItem);
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

  public ListDataBundlesResponse nextPageToken(String nextPageToken) {
    this.nextPageToken = nextPageToken;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ListDataBundlesResponse {\n");
    
    sb.append("    dataBundles: ").append(toIndentedString(dataBundles)).append("\n");
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

