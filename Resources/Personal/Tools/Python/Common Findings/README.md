# Common Findings

A Python script (`common_findings.py`) designed to perform a basic security assessment of a target website. It checks for the presence of common sensitive files and directories, analyzes HTTP headers for security configurations, verifies SSL/TLS setups, and extracts links from the homepage. The results are displayed in a user-friendly format and saved to a CSV file for further analysis.

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Output](#output)
* [Example](#example)
* [Contributing](#contributing)
* [License](#license)

## Features

* Common Files and Directories Check: Scans for the existence of sensitive files and directories that are commonly targeted by attackers
* Security Headers Analysis: Evaluates HTTP headers to ensure essential security configurations are in place
* SSL/TLS Verification: Checks if the website has proper SSL/TLS configurations
* Link Extraction: Gathers all hyperlinks from the homepage for further examination
* Concurrent Execution: Utilizes threading to perform checks simultaneously, reducing overall scan time
* Rich Output: Presents findings in formatted tables using the rich library for enhanced readability
* CSV Export: Saves all findings to a findings.csv file for easy reference and reporting

## Prerequisites

* Python 3.6 or higher
* Internet connection to perform web requests

## Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/common_findings.git
cd common_findings
```

2. Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt, install the dependencies manually:

```bash
pip install requests urllib3 beautifulsoup4 rich
```

## Usage

1. Run the Script

```bash
python common_findings.py
```

2. Enter the Target URL

When prompted, input the URL of the website you wish to scan. Ensure you include the protocol (http:// or https://).

```bash
Enter Target URL: https://example.com
```

3. View Results

The script will perform various checks and display the results in the console using formatted tables. Additionally, all findings will be saved to a findings.csv file in the script's directory.

## Output

The script provides two types of output:

### Console Output

Displays four main sections:
* Common Files and Directories: Lists each file/directory checked along with its status (Found/Not Found)
* Headers: Shows the HTTP headers returned by the server and highlights missing security headers
* SSL/TLS Configuration: Indicates whether SSL/TLS is properly configured
* Extracted Links: Lists all hyperlinks found on the homepage

### CSV File (findings.csv)

Contains a consolidated list of all findings with the following columns:
* URL: The target URL or the specific endpoint checked
* Status: The result of the check (e.g., Found, Not Found, Missing Header)
* Details: Additional information related to the finding

## Example

```bash
$ python common_findings.py
Enter Target URL: https://example.com

[*] Checking common files and directories on https://example.com
[*] Checking headers for security configurations on https://example.com
[*] Checking SSL/TLS configuration on https://example.com
[*] Extracting links from https://example.com

[+] Common Files and Directories:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ URL                                    ┃ Status    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ https://example.com/.env                │ Not Found │
│ https://example.com/config.php          │ Found     │
└────────────────────────────────────────┴───────────┘

[+] Headers:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ URL                                    ┃ Status                               ┃ Details                                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ https://example.com                    │ Headers                              │ { 'Content-Type': 'text/html; charset=UTF-8', ... } │
│ https://example.com                    │ Missing X-Frame-Options header       │                                                     │
└────────────────────────────────────────┴─────────────────────────────────────┴────────────────────────────────────────────────────────┘

[+] SSL/TLS Configuration:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ URL                                    ┃ Status                               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ https://example.com                    │ SSL/TLS configuration is in place    │
└────────────────────────────────────────┴─────────────────────────────────────┘

[+] Extracted Links:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ URL                                    ┃ Status                               ┃ Details                                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ https://example.com                    │ Found link                           │ /about                                             │
│ https://example.com                    │ Found link                           │ https://external.com/contact                       │
└────────────────────────────────────────┴─────────────────────────────────────┴────────────────────────────────────────────────────────┘

[+] Findings saved to findings.csv
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the Repository
2. Create a New Branch
```bash
git checkout -b feature/YourFeature
```
3. Commit Your Changes
```bash
git commit -m "Add your message"
```
4. Push to the Branch
```bash
git push origin feature/YourFeature
```
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Additional Notes

* Repository Name: Ensure that your GitHub repository is named appropriately, for example, `common_findings`, to match the project description.
* requirements.txt: To make installation easier, create a requirements.txt file with the following content:

```text
requests
urllib3
beautifulsoup4
rich
```

This allows users to install all dependencies with a single command:

```bash
pip install -r requirements.txt
```

* Script Location: Place `common_findings.py` at the root of your repository so that users can run it directly after cloning.
* License File: Don't forget to include a LICENSE file in your repository to specify the project's licensing terms.
