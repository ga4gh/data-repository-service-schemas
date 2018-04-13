package ga4gh.dos;

import ga4gh.dos.DataBundle;
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

public class GetDataBundleVersionsResponse  {
  
  @ApiModelProperty(value = "REQUIRED All versions of the Data Bundles that match the GetDataBundleVersions request.")
 /**
   * REQUIRED All versions of the Data Bundles that match the GetDataBundleVersions request.  
  **/
  private List<DataBundle> dataBundles = null;
 /**
   * REQUIRED All versions of the Data Bundles that match the GetDataBundleVersions request.
   * @return dataBundles
  **/
  @JsonProperty("data_bundles")
  public List<DataBundle> getDataBundles() {
    return dataBundles;
  }

  public void setDataBundles(List<DataBundle> dataBundles) {
    this.dataBundles = dataBundles;
  }

  public GetDataBundleVersionsResponse dataBundles(List<DataBundle> dataBundles) {
    this.dataBundles = dataBundles;
    return this;
  }

  public GetDataBundleVersionsResponse addDataBundlesItem(DataBundle dataBundlesItem) {
    this.dataBundles.add(dataBundlesItem);
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class GetDataBundleVersionsResponse {\n");
    
    sb.append("    dataBundles: ").append(toIndentedString(dataBundles)).append("\n");
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

