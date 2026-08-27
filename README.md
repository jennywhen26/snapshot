# snapshot ![Version](https://img.shields.io/badge/version-0.1.2-blue)
# documentation [![Python Check](https://github.com/jennywhen26/filesystem-name-inspector/actions/workflows/main.yml/badge.svg)](https://github.com/jennywhen26/filesystem-name-inspector/actions/workflows/main.yml)
 
## (Media Carrier Intake Snapshot Tool)
 
## Summary
 
Snapshot is a Python command-line tool that creates a comprehensive preservation snapshot of media carriers when they arrive at your institution. It automates the ingestion workflow by running preservation and analysis tools, capturing their output, and giving you the option to save results. The tool scans for viruses, generates hash sums (checksums), maps directory structures, and extracts technical metadata in one streamlined process.
 
## Installation and Dependencies
 
### Requirements
 
- Python 3.7 or higher
- Homebrew (for installing external tools)

### External Dependencies
 
Install the following tools via Homebrew:
 
```bash
brew install clamav      # Virus and malware detection
brew install md5deep     # Checksums (hashdeep)
brew install tree        # Directory structure mapping
brew install exiftool    # Metadata extraction
```
 
### Python Libraries Used
 
- *subprocess*: Execute external preservation tools
- *os.path*: File and directory operations
- *pathlib*: Cross-platform path handling

## What Does the Script Do?
 
The script automates the following preservation workflow:
 
1. **Virus Scanning** (clamscan) - Detects malware and viruses
2. **Checksum Generation** (hashdeep) - Creates MD5 and SHA256 checksums in XML format
3. **Directory Mapping** (tree) - Documents complete directory structure
4. **Metadata Extraction** (exiftool) - Captures technical metadata from media files
Results can be saved with standardized naming conventions for easy tracking and archival.
 
## How to Use?
 
### On macOS/Linux
 
```bash
python3 snapshot_v0-1-2.py
```
 
### On Windows
 
```bash
python snapshot_v0-1-2.py
```
 
### Interactive Workflow
 
```
Snapshot v0.1.2
 
Please enter path to the media carrier/directory: /Volumes/ExternalDrive
Run clamscan? (y/n): y
running clamscan...please wait!
[virus scan results...]
 
Run hashdeep? (y/n): y
running hashdeep...please wait!
[checksum results...]
 
Run tree? (y/n): y
[directory structure...]
 
Run exiftool? (y/n): y
[metadata extraction...]
 
Would you like to save your results? (y/n): y
```
 
### User Input
 
- **Media path**: Full path to the media carrier or directory to scan
- **Service selection**: Run each tool (y/n for each service)
- **Save location**: Directory where preservation records will be saved
- **Component information**: Date (YYYYMMDD) and component number (e.g., 2002-228-ECx1)
## Output Files
 
Results are saved with standardized naming convention:
 
```
{component_number}_{date}-delivery_{service}.{extension}
```
 
### Example Output Filenames
 
- `2002-228-ECx1_20260827-delivery_clamscan.txt`
- `2002-228-ECx1_20260827-delivery_hashdeep.xml`
- `2002-228-ECx1_20260827-delivery_tree.txt`
- `2002-228-ECx1_20260827-delivery_exiftool.txt`

### File Formats
 
- **clamscan** - Plain text listing of scanned files and results
- **hashdeep** - DFXML (Digital Forensics XML) format with cryptographic checksums
- **tree** - Hierarchical directory structure with file information
- **exiftool** - Technical metadata from media files (images, videos, documents)
## Known Limitations
 
### Metadata Encoding Issues
 
Some media files store metadata in legacy character encodings (such as GB2312, Big5, GBK, or other regional standards) rather than UTF-8. When exiftool extracts this metadata, these fields appear garbled in the output (e.g., "¹¸¹û..." instead of proper characters).
 
The script uses latin-1 encoding, which accepts all byte values (0-255) without crashing, but displays non-UTF-8 bytes as garbled text. This is a limitation of the source files' legacy encoding, not the script.
 
**Why this happens:** Some media files use legacy character encodings (such as GB2312, Big5, GBK, or other regional encodings) that predate UTF-8 standards. When the script reads these legacy-encoded bytes using UTF-8, Python encounters invalid byte sequences. The script uses Latin-1 as a fallback because Latin-1 accepts all byte values (0-255) without crashing, as it treats each byte as a separate character rather than a multi-byte sequence. However, since Latin-1 isn't the actual encoding of the legacy-encoded metadata, the output appears garbled.
If you need to decode garbled metadata, consider using encoding detection tools like chardet or iconv to identify and convert the correct encoding.
 
**What this means for your workflow:**
- ✓ The script completes successfully
- ✓ All metadata is captured (even if unreadable)
- ✗ Non-UTF-8 characters appear garbled
- This matches the output you would see running exiftool directly in the terminal

### External Drive Performance
 
For large external drives, hashdeep and exiftool may take several minutes to complete. The script does not display real-time progress during processing. This is normal behavior for large media collections.
 
## Troubleshooting
 
### "Command not found: snapshot"
 
The script must be in your PATH or run directly:
```bash
python3 /path/to/snapshot_v0-1-2.py
```
 
### "Path invalid. Please try again."
 
Check that:
- The path exists and is readable
- Remove trailing spaces from paths: `/Volumes/Drive /` → `/Volumes/Drive`
- Use quotes for paths with spaces: `"/Volumes/My Drive"`

### "clamscan: command not found" or other tool not found
 
Install the missing tool:
```bash
brew install clamav        # For clamscan
brew install md5deep       # For hashdeep
brew install tree          # For tree
brew install exiftool      # For exiftool
```
 
### Freshclam Update Fails
 
Freshclam may fail if:
- No internet connection
- ClamAV update servers temporarily unavailable
- Database already up-to-date
The script will ask if you want to continue with clamscan using existing virus definitions. This is safe and normal.
 
### Results Show Garbled Characters
 
This is a metadata encoding issue (see Known Limitations). The data is preserved but not human-readable for non-UTF-8 content. The script is working correctly.
 
## Version History
 
### v0.1.2 (August 27, 2026)
- Fixed exiftool error handling to save results even when warnings occur
- Added latin-1 encoding for better compatibility with mixed-encoding files and to prevent exiftool from crashing
- Improved error messages for encoding issues
- Fixed backslash escape issue in file paths
- Documented metadata encoding limitations in README
### v0.1.1 (August 20, 2026)


### v0.1.0 (August 15, 2026)
- Initial release
- Core functionality: clamscan, hashdeep, tree, exiftool
- Interactive prompts and standardized file output

## Technical Details
 
### Exit Codes
 
- `0` - Successful completion
- `1` - User exited during workflow
- Non-zero from tools - Tool-specific warnings/errors (script continues with results anyway)

### Python Modules
 
- subprocess - Execute external tools and capture output
- os.path - File and directory operations
- pathlib - Cross-platform file path handling

## Support
 
For issues with specific tools:
- **clamscan/freshclam** - See [ClamAV documentation](https://www.clamav.net/)
- **hashdeep** - See [md5deep documentation](https://md5deep.sourceforge.io/)
- **tree** - Run `man tree`
- **exiftool** - See [ExifTool documentation](https://exiftool.org/)
  
## License
 
MIT License
 
## Maintainer
 
Jenny Hsu @jennywhen26
 
#### The script was developed with the help of Claude, which is an AI assistant built by Anthropic.
