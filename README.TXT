# Email Unsubscribe Link Extractor

This Python script connects to an email account, searches for emails containing "unsubscribe" links, extracts those links, attempts to visit them, and saves them to a text file.

## Features

- Connects to a Gmail account using IMAP.
- Searches for emails containing "unsubscribe" links.
- Extracts and attempts to visit each link.
- Saves the extracted links to a file named `links.txt`.

## Requirements

To run this script, you need to have the following Python packages installed:

- `requests`
- `beautifulsoup4`
- `python-dotenv`

You can install these packages using pip:

```bash
pip install requests beautifulsoup4 python-dotenv
