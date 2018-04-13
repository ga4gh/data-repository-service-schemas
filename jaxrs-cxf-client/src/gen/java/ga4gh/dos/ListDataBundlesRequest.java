package ga4gh.dos;

import ga4gh.dos.Checksum;
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
  * Only return Data Bundles that match all of the request parameters. A page_size and page_token are provided for retrieving a large number of results.
 **/
@ApiModel(description="Only return Data Bundles that match all of the request parameters. A page_size and page_token are provided for retrieving a large number of results.")
public class ListDataBundlesRequest  {
  
  @ApiModelProperty(value = "OPTIONAL If provided returns Data Bundles that have any alias that matches the request.")
 /**
   * OPTIONAL If provided returns Data Bundles that have any alias that matches the request.  
  **/
  private String alias = null;

  @ApiModelProperty(value = "OPTIONAL If provided, will only return Data Bundles which have the provided checksum.")
 /**
   * OPTIONAL If provided, will only return Data Bundles which have the provided checksum.  
  **/
  private Checksum checksum = null;

  @ApiModelProperty(value = "OPTIONAL Specifies the maximum number of results to return in a single page. If unspecified, a system default will be used.")
 /**
   * OPTIONAL Specifies the maximum number of results to return in a single page. If unspecified, a system default will be used.  
  **/
  private Integer pageSize = null;

  @ApiModelProperty(value = "OPTIONAL The continuation token, which is used to page through large result sets. To get the next page of results, set this parameter to the value of `next_page_token` from the previous response.")
 /**
   * OPTIONAL The continuation token, which is used to page through large result sets. To get the next page of results, set this parameter to the value of `next_page_token` from the previous response.  
  **/
  private String pageToken = null;
 /**
   * OPTIONAL If provided returns Data Bundles that have any alias that matches the request.
   * @return alias
  **/
  @JsonProperty("alias")
  public String getAlias() {
    return alias;
  }

  public void setAlias(String alias) {
    this.alias = alias;
  }

  public ListDataBundlesRequest alias(String alias) {
    this.alias = alias;
    return this;
  }

 /**
   * OPTIONAL If provided, will only return Data Bundles which have the provided checksum.
   * @return checksum
  **/
  @JsonProperty("checksum")
  public Checksum getChecksum() {
    return checksum;
  }

  public void setChecksum(Checksum checksum) {
    this.checksum = checksum;
  }

  public ListDataBundlesRequest checksum(Checksum checksum) {
    this.checksum = checksum;
    return this;
  }

 /**
   * OPTIONAL Specifies the maximum number of results to return in a single page. If unspecified, a system default will be used.
   * @return pageSize
  **/
  @JsonProperty("page_size")
  public Integer getPageSize() {
    return pageSize;
  }

  public void setPageSize(Integer pageSize) {
    this.pageSize = pageSize;
  }

  public ListDataBundlesRequest pageSize(Integer pageSize) {
    this.pageSize = pageSize;
    return this;
  }

 /**
   * OPTIONAL The continuation token, which is used to page through large result sets. To get the next page of results, set this parameter to the value of &#x60;next_page_token&#x60; from the previous response.
   * @return pageToken
  **/
  @JsonProperty("page_token")
  public String getPageToken() {
    return pageToken;
  }

  public void setPageToken(String pageToken) {
    this.pageToken = pageToken;
  }

  public ListDataBundlesRequest pageToken(String pageToken) {
    this.pageToken = pageToken;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ListDataBundlesRequest {\n");
    
    sb.append("    alias: ").append(toIndentedString(alias)).append("\n");
    sb.append("    checksum: ").append(toIndentedString(checksum)).append("\n");
    sb.append("    pageSize: ").append(toIndentedString(pageSize)).append("\n");
    sb.append("    pageToken: ").append(toIndentedString(pageToken)).append("\n");
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

