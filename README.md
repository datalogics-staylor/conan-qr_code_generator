# conan-qr_code_generator
Conan packaging for the Nayuki QR-Code-generator

## Versioning

The version number is not included in the `conanfile.py`; supply the version number when creating the package, or exporting or creating a package. Examples:

- `conan install . 1.5.0@kam/testing`
- `conan export . 1.5.0@datalogics/stable`
- `conan create . 1.5.0@datalogics/table`

(Of course, add other argument as required for the profile, install folder, and so forth.)

### Adding a version

The `conanfile.py` uses the `conandata.yml` file to obtain the URL of the source tarball and the checksum of that tarball. If adding a new version, simply add a new entry, keyed by the version number.

Then export the recipe with the version number as above, and upload it.
