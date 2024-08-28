# ICP Data Center Verification

This Python script verifies whether the IP addresses of nodes in a data center are correctly advertised in the expected country by using RDAP lookups.

## Features
- Fetch data center information using the Internet Computer API.
- Retrieve node details from the specified data center.
- Perform RDAP lookups to verify the country associated with the IP addresses.
- Supports different RDAP servers based on the region (Asia, America, Europe).
- Provides a summary of nodes that are correctly advertised and lists any issues found.

## Requirements

- Python 3.8 or later
- Required Python packages listed in `requirements.txt`

## Installation

1. **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd icp-dc-verification
    ```

2. **Set Up a Virtual Environment (Optional but Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Script:**
    ```bash
    python main.py
    ```

2. **Enter the Data Center ID:**
    When prompted, enter the data center ID (e.g., `cm1`). The script will fetch data from the Internet Computer API, perform RDAP lookups, and provide a summary of the results.

## Example Output

```plaintext
Enter Data Center ID (e.g., cm1): cm1
Data Center Country: LK, Region: Asia
Checking IP: XXX, Subnet: XXX::/64
RDAP Country: LK
IP XXX is correctly advertised in LK.

Summary:
Nodes correctly advertised in LK: 4
Issues found: 0
