package ga4gh.dos;

import ga4gh.dos.DataBundle;

import io.swagger.annotations.ApiModelProperty;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import com.fasterxml.jackson.annotation.JsonProperty;

public class CreateDataBundleRequest  {
  
  @ApiModelProperty(value = "")
  private DataBundle dataBundle = null;
 /**
   * Get dataBundle
   * @return dataBundle
  **/
  @JsonProperty("data_bundle")
  public DataBundle getDataBundle() {
    return dataBundle;
  }

  public void setDataBundle(DataBundle dataBundle) {
    this.dataBundle = dataBundle;
  }

  public CreateDataBundleRequest dataBundle(DataBundle dataBundle) {
    this.dataBundle = dataBundle;
    return this;
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class CreateDataBundleRequest {\n");
    
    sb.append("    dataBundle: ").append(toIndentedString(dataBundle)).append("\n");
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

