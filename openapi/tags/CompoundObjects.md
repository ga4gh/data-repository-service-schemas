## Compound Objects

Common examples of compound objects in biomedicine include:
* BAM+BAI genomic reads, with a small index (the BAI object) to large data (the BAM object), each object using a well-defined file format.
* DICOM images, with a contents object pointing to one or more raw image objects, each containing pixels from different aspects of a single logical biomedical image (e.g. different z-coordinates)
* studies, with a single table of contents listing multiple objects of various types that were generated together and are meant to be processed together

As with single objects, DRS clients and servers are expected to agree on the semantics of individual compound objects using non-DRS mechanisms. The recommended best practice for representing a particular compound object type is:
1. Define a manifest file syntax, which contains a list of the DRS IDs of the leaf objects, plus type-specific information about the relationship between the different elements of the compound object.
2. Make manifest objects, and each of their referenced leaf objects, available using standard DRS mechanisms -- each manifest and each leaf are referenced via their own DRS IDs, just like any other single object.
3. Document the expected client logic for processing compound objects of interest. This logic typically consists of using standard DRS mechanisms to fetch the manifest, parsing its syntax, extracting the DRS IDs of leaf objects, and using standard DRS mechanisms to fetch relevant leaf objects.
