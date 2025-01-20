#!/usr/local/bin/python3
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import os
import threading
import csv
from rich.console import Console
from rich.table import Table
from rich import print

# Suppress only the single InsecureRequestWarning from urllib3 needed to verify SSL/TLS
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Clear console
os.system('cls' if os.name == 'nt' else 'clear')

TARGET_URL = input("Enter Target URL: ").rstrip('/')  # Remove trailing slash from the target URL

# Initialize console for rich output
console = Console()

# List of common files and directories to check
COMMON_FILES = [
    '.env', 'config.php', 'settings.py', 'web.config', 'application.yml', 'config.json',
    'backup.zip', 'db_backup.sql', '.bak', '.old', '.tmp', 'error.log', 'access.log',
    'debug.log', 'id_rsa', 'id_rsa.pub', '.ssh/', 'keys/', 'secrets/', 'robots.txt',
    '.htaccess', '.git/', '.DS_Store', 'crossdomain.xml', 'sitemap.xml', 'admin/',
    'login/', 'register/', 'dashboard/', 'user/', 'api/'
]

findings_common = []
findings_headers = []
findings_ssl_tls = []
findings_links = []

# Function to check for common files and directories
def check_common_files(url):
    for file in COMMON_FILES:
        full_url = f'{url}/{file}'
        response = requests.get(full_url, verify=False)
        if response.status_code == 200:
            findings_common.append((full_url, 'Found'))
        else:
            findings_common.append((full_url, 'Not Found'))

# Function to check headers for security configurations
def check_headers(url):
    response = requests.get(url, verify=False)
    headers = response.headers
    findings_headers.append((url, 'Headers', headers))
    # Check for some common security headers
    if 'X-Frame-Options' not in headers:
        findings_headers.append((url, 'Missing X-Frame-Options header'))
    if 'Content-Security-Policy' not in headers:
        findings_headers.append((url, 'Missing Content-Security-Policy header'))
    if 'Strict-Transport-Security' not in headers:
        findings_headers.append((url, 'Missing Strict-Transport-Security header'))

# Function to check SSL/TLS configuration
def check_ssl_tls(url):
    response = requests.get(url, verify=False)
    if response.url.startswith('https'):
        findings_ssl_tls.append((url, 'SSL/TLS configuration is in place'))
    else:
        findings_ssl_tls.append((url, 'SSL/TLS configuration is not in place'))

# Function to extract links from the homepage for further checks
def extract_links(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    for link in links:
        findings_links.append((url, 'Found link', link))

def save_to_csv(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Status", "Details"])
        for finding in findings_common + findings_headers + findings_ssl_tls + findings_links:
            writer.writerow(finding)

def main():
    threads = []

    console.print(f'[*] Checking common files and directories on {TARGET_URL}', style='bold green')
    thread = threading.Thread(target=check_common_files, args=(TARGET_URL,))
    threads.append(thread)
    thread.start()

    console.print(f'\n[*] Checking headers for security configurations on {TARGET_URL}', style='bold green')
    thread = threading.Thread(target=check_headers, args=(TARGET_URL,))
    threads.append(thread)
    thread.start()

    console.print(f'\n[*] Checking SSL/TLS configuration on {TARGET_URL}', style='bold green')
    thread = threading.Thread(target=check_ssl_tls, args=(TARGET_URL,))
    threads.append(thread)
    thread.start()

    console.print(f'\n[*] Extracting links from {TARGET_URL}', style='bold green')
    thread = threading.Thread(target=extract_links, args=(TARGET_URL,))
    threads.append(thread)
    thread.start()

    for thread in threads:
        thread.join()

    console.print('\n[+] Common Files and Directories:', style='bold blue')
    table_common = Table(show_header=True, header_style="bold magenta")
    table_common.add_column("URL", style="dim", width=50, overflow="fold")
    table_common.add_column("Status")

    for finding in findings_common:
        table_common.add_row(*map(str, finding))

    console.print(table_common)

    console.print('\n[+] Headers:', style='bold blue')
    table_headers = Table(show_header=True, header_style="bold magenta")
    table_headers.add_column("URL", style="dim", width=50, overflow="fold")
    table_headers.add_column("Status")
    table_headers.add_column("Details", overflow="fold")

    for finding in findings_headers:
        table_headers.add_row(*map(str, finding))

    console.print(table_headers)

    console.print('\n[+] SSL/TLS Configuration:', style='bold blue')
    table_ssl_tls = Table(show_header=True, header_style="bold magenta")
    table_ssl_tls.add_column("URL", style="dim", width=50, overflow="fold")
    table_ssl_tls.add_column("Status")

    for finding in findings_ssl_tls:
        table_ssl_tls.add_row(*map(str, finding))

    console.print(table_ssl_tls)

    console.print('\n[+] Extracted Links:', style='bold blue')
    table_links = Table(show_header=True, header_style="bold magenta")
    table_links.add_column("URL", style="dim", width=50, overflow="fold")
    table_links.add_column("Status")
    table_links.add_column("Details", overflow="fold")

    for finding in findings_links:
        table_links.add_row(*map(str, finding))

    console.print(table_links)

    save_to_csv('findings.csv')
    console.print(f'\n[+] Findings saved to findings.csv', style='bold blue')

if __name__ == '__main__':
    main()
