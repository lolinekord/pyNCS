# pyNCS - All songs downloader script for NCS lovers.
# Usage
It is written very succinctly and can be easily manipulated using command line arguments.

## Install all required dependencies

    pip install -r requirements.txt

## Run main.py in the project directory.

### Archive the latest information from the [official website](https://ncs.io/):

    python3 main.py --mode fetch

### Extracting song listings from archived HTML files:

    python3 main.py --mode parse

### Download all data based on the extracted song list (tid):

    python3 main.py --mode download


That's it! All your songs should now be downloaded.

# Disclaimer
The creator, [lolineko](https://lolineko3.net), does not take any responsibility for any damages caused by the use of this script.
I would like to extend my sincere gratitude to the official site, [ncs.io](https://ncs.io), and apologize for the increased traffic.

# Lisence
pyNCS is licensed under the MIT License.
