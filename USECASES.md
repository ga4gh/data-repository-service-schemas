# Overview

A place to document our use cases for Data Object Service (DOS).

The Cromwell group has 4 instances via 2 projects where DOS is being considered. These are all similar enough to effectively be a single use case. We need to model an institution's local storage as a private cloud exposing basic read/write/sizeof functionality akin to GCS or S3. For instance instead of `gs:this/is/my/bucket` it'd be `site1:this/is/my/bucket` or `site2:this/is/my/bucket`. While these use cases don't *need* human readability the stakeholders have expressed preferences towards this over UUID approaches. Similar stances have been taken regarding putting a redirection utility in front of these private clouds.
