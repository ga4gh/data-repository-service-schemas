package ga4gh.dos;

import ga4gh.dos.ChecksumRequest;
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
  * Allows a requester to list and filter Data Objects. Only Data Objects matching all of the requested parameters will be returned.
 **/
@ApiModel(description="Allows a requester to list and filter Data Objects. Only Data Objects matching all of the requested parameters will be returned.")
public class ListDataObjectsRequest  {
  
  @ApiModelProperty(value = "OPTIONAL If provided will only return Data Objects with the given alias.")
 /**
   * OPTIONAL If provided will only return Data Objects with the given alias.  
  **/
  private String alias = null;

  @ApiModelProperty(value = "OPTIONAL If provided will return only Data Objects with a that URL matches this string.")
 /**
   * OPTIONAL If provided will return only Data Objects with a that URL matches this string.  
  **/
  private String url = null;

  @ApiModelProperty(value = "OPTIONAL If provided will only return data object messages with the provided checksum. If the checksum type is provided")
 /**
   * OPTIONAL If provided will only return data object messages with the provided checksum. If the checksum type is provided  
  **/
  private ChecksumRequest checksum = null;

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
   * OPTIONAL If provided will only return Data Objects with the given alias.
   * @return alias
  **/
  @JsonProperty("alias")
  public String getAlias() {
    return alias;
  }

  public void setAlias(String alias) {
    this.alias = alias;
  }

  public ListDataObjectsRequest alias(String alias) {
    this.alias = alias;
    return this;
  }

 /**
   * OPTIONAL If provided will return only Data Objects with a that URL matches this string.
   * @return url
  **/
  @JsonProperty("url")
  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public ListDataObjectsRequest url(String url) {
    this.url = url;
    return this;
  }

 /**
   * OPTIONAL If provided will only return data object messages with the provided checksum. If the checksum type is provided
   * @return checksum
  **/
  @JsonProperty("checksum")
  public ChecksumRequest getChecksum() {
    return checksum;
  }

  public void setChecksum(ChecksumRequest checksum) {
    this.checksum = checksum;
  }

  public ListDataObjectsRequest checksum(ChecksumRequest checksum) {
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

  public ListDataObjectsRequest pageSize(Integer pageSize) {
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

  public ListDataObjectsRequest pageToken(String pageToken) {
    this.pageToken = pageToken;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ListDataObjectsRequest {\n");
    
    sb.append("    alias: ").append(toIndentedString(alias)).append("\n");
    sb.append("    url: ").append(toIndentedString(url)).append("\n");
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

