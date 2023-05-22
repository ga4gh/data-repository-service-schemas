## Compound Objects

The DRS API supports access to data objects, with each `DrsObject` representing a single opaque blob of bytes. Much content (e.g. VCF files) is well represented as a single atomic `DrsObject`. Some content, however (e.g. DICOM images) is best represented as a compound object consisting of a structured collection of atomic `DrsObject`s. In both cases, DRS isn't aware of the semantics of the objects it serves -- understanding those semantics is the responsibility of the applications that call DRS.

Common examples of compound objects in biomedicine include:
* BAM+BAI genomic reads, with a small index (the BAI object) to large data (the BAM object), each object using a well-defined file format.
* DICOM images, with a contents object pointing to one or more raw image objects, each containing pixels from different aspects of a single logical biomedical image (e.g. different z-coordinates)
* studies, with a single table of contents listing multiple objects of various types that were generated together and are meant to be processed together

## Best Practice: Manifests

As with atomic objects, DRS applications and servers are expected to agree on the semantics of compound objects using non-DRS mechanisms. The recommended best practice for representing a particular compound object type is:
1. Define a manifest file syntax, which contains the DRS IDs of the constituent atomic objects, plus type-specific information about the relationship between those constituents.
    * Manifest file syntax isn't prescribed by the spec, but we expect they will often be JSON files.
    * For example, for a BAM+BAI pair the manifest file could contain two key-value pairs mapping the type of each constituent file to its DRS ID.
3. Make manifest objects and their constituent objects available using standard DRS mechanisms -- each object is referenced via its own DRS ID, just like any other atomic object.
    * For example, for a BAM+BAI pair, there would be three DRS IDs -- one for the manifest, one for the BAM, and one for the BAI.
5. Document the expected client logic for processing compound objects of interest. This logic typically consists of using standard DRS mechanisms to fetch the manifest, parsing its syntax, extracting the DRS IDs of constituent objects, and using standard DRS mechanisms to fetch the constituents as needed.
    * In some cases the application will always want to fetch all of the constituents; in other cases it may want to initially fetch a subset, and only fetch the others on demand. For example, a DICOM image viewer may only want to fetch the layers that are being rendered.
