# PubChem CAS ↔ CID Converter

A Python utility for bidirectional conversion between CAS numbers and PubChem Compound IDs (CIDs) with local caching for efficient repeated queries.

## Features

- **CAS to PubChem CID**: Retrieve PubChem IDs using CAS registry numbers
- **PubChem CID to CAS**: Lookup CAS numbers from PubChem Compound IDs
- **Local Caching**: Automatically caches results in `pubchemid_cas_cache.csv` to:
  - Reduce API calls to PubChem
  - Improve performance for repeated queries
  - Maintain a local lookup database

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pubchem-cas-cid-converter.git
   cd pubchem-cas-cid-converter
Install required dependencies:

bash
pip install pandas requests
Usage
python
from pubchem_converter import get_pubchemid_by_cas, get_cas_by_pubchemid

# Get PubChem CID from CAS number
pubchem_id = get_pubchemid_by_cas('7732-18-5')  # Returns 962 for water

# Get CAS number from PubChem CID
cas_number = get_cas_by_pubchemid(962)  # Returns '7732-18-5'
Cache Management
The script automatically creates and maintains a cache file (pubchemid_cas_cache.csv) in the working directory. This file stores all successful lookups for future reference.

To clear the cache, simply delete the file or create a new empty file with the same name.

# Error Handling
The functions will:

Return None if the lookup fails

Print error messages to console for debugging

Continue functioning with cached data even if network requests fail

# Requirements
Python 3.6+

pandas

requests

# License
MIT License - Free for personal and commercial use
