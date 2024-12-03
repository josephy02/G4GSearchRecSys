import os
import csv
from bs4 import BeautifulSoup
from pathlib import Path
import re

def clean_folder_name(folder_name):
    """Convert folder name to readable title."""
    # Replace hyphens and underscores with spaces
    clean_name = folder_name.replace('-', ' ').replace('_', ' ')
    # Remove any trailing dots and text after them (from truncated names)
    clean_name = re.sub(r'\.+.*$', '', clean_name)
    # Capitalize words
    clean_name = ' '.join(word.capitalize() for word in clean_name.split())
    return clean_name

def extract_text_from_html(file_path):
    """Extract text content from HTML files."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get the main content (adjusting for GeeksForGeeks structure)
        main_content = (
            soup.find('article') or
            soup.find('div', class_='article-wrapper') or
            soup.find('div', class_='entry-content') or
            soup.find('div', class_='content')
        )

        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)

        # Extract title
        title_elem = (
            soup.find('h1', class_='article-title') or
            soup.find('h1') or
            soup.title
        )
        title = title_elem.get_text(strip=True) if title_elem else ''

        # Extract URL (try different methods)
        url = ''
        # Try canonical URL first
        canonical = soup.find('link', {'rel': 'canonical'})
        if canonical:
            url = canonical.get('href', '')
        # Try og:url if canonical not found
        if not url:
            og_url = soup.find('meta', {'property': 'og:url'})
            if og_url:
                url = og_url.get('content', '')
        # Try actual link if neither found
        if not url:
            actual_link = soup.find('meta', {'property': 'article:published_link'})
            if actual_link:
                url = actual_link.get('content', '')

        return {
            'title': title,
            'content': text,
            'url': url
        }

def clean_text(text):
    """Clean extracted text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def process_geeks_directory(root_folder, output_file):
    """Process GeeksForGeeks directory structure and save to CSV."""
    processed_data = []
    doc_counter = 0

    # Walk through the directory structure
    for root, dirs, files in os.walk(root_folder):
        # Skip the root directory itself
        if root == root_folder:
            continue

        # Get the immediate parent folder name as the topic
        topic_folder = os.path.basename(root)
        topic = clean_folder_name(topic_folder)

        # Process index.html if it exists
        if 'index.html' in files:
            file_path = os.path.join(root, 'index.html')
            try:
                # Extract content
                data = extract_text_from_html(file_path)

                # Clean the extracted text
                data['content'] = clean_text(data['content'])
                data['title'] = clean_text(data['title'])

                # Add metadata
                data['docid'] = f"{doc_counter}"
                data['topic'] = topic
                data['folder_path'] = root
                data['relative_path'] = os.path.relpath(root, root_folder)

                processed_data.append(data)
                print(f"Processed: {topic} (ID: {data['docid']})")

                doc_counter += 1  # Increment counter for next document

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

    # Write to CSV
    if processed_data:
        fieldnames = ['docid', 'title', 'topic', 'content', 'url', 'folder_path', 'relative_path']
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_data)
        print(f"\nSuccessfully saved {len(processed_data)} entries to {output_file}")
    else:
        print("No data was processed!")

# Example usage
if __name__ == "__main__":
    input_folder = "/Users/joeyared/Desktop/INFO_376/geek"  # Replace with your folder path if different
    output_file = "./data/geeksforgeeks_articles.csv"
    process_geeks_directory(input_folder, output_file)