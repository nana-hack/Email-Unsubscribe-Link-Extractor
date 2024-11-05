from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import imaplib
import email

# Load environment variables
load_dotenv()

# Get email credentials from environment variables
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def connect_to_mail():
    """Connect to the email server and return the connection object."""
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail

def extract_links_from_html(html_content):
    """Extract unsubscribe links from the given HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [link["href"] for link in soup.find_all('a', href=True) if "unsubscribe" in link["href"].lower()]
    return links

def click_link(link):
    """Attempt to visit the given link and print the result."""
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print("Successfully visited", link)
        else:
            print("Failed to visit", link, "error code", response.status_code)
    except Exception as e:
        print("Error with", link, str(e))

def search_for_email():
    """Search for emails containing unsubscribe links and return the links."""
    mail = connect_to_mail()
    links = []

    try:
        # Search for emails containing "unsubscribe" in the body
        _, search_data = mail.search(None, '(BODY "unsubscribe")')
        data = search_data[0].split()

        for num in data:
            _, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            # Check if the email is multipart
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        html_content = part.get_payload(decode=True).decode()
                        links.extend(extract_links_from_html(html_content))
            else:
                content_type = msg.get_content_type()
                content = msg.get_payload(decode=True).decode()

                if content_type == "text/html":
                    links.extend(extract_links_from_html(content))
    finally:
        mail.logout()  # Ensure the connection is closed

    return links

def save_links(links):
    """Save the extracted links to a text file."""
    with open("links.txt", "w") as f:
        f.write("\n".join(links))

# Main execution
if __name__ == "__main__":
    links = search_for_email()
    if links:  # Check if there are links to click
        for link in links:
            click_link(link)

    save_links(links)