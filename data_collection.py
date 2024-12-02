import os
import csv
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

# Directory containing HTML, HTM, and PDF files
data_dir = "/Users/joeyared/Desktop/INFO_376/geek"

# Initialize a list to store extracted data
data = []

def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        url = soup.find("meta", {"property": "og:url"})["content"] if soup.find("meta", {"property": "og:url"}) else "N/A"
        title = soup.title.string if soup.title else "N/A"
        rating = 0  # Placeholder for ratings
        content = soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "N/A"
        tags = {tag.string for tag in soup.find_all("meta", {"name": "keywords"})} if soup.find_all("meta", {"name": "keywords"}) else set()

        return {
            "url": url,
            "title": title,
            "rating": rating,
            "content": content,
            "tags": ", ".join(tags)  # Convert set to a comma-separated string
        }

def process_pdf_file(file_path):
    try:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() for page in reader.pages)
        title = os.path.basename(file_path).replace(".pdf", "").title()  # Use file name as title
        rating = 0  # Placeholder for ratings
        tags = set()  # Placeholder for tags

        return {
            "url": "N/A",  # PDFs may not have a specific URL
            "title": title,
            "rating": rating,
            "content": text[:5000],  # Truncate to first 5000 characters for brevity
            "tags": ", ".join(tags)
        }
    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")
        return None

# Iterate through files in the directory
for filename in os.listdir(data_dir):
    file_path = os.path.join(data_dir, filename)

    if filename.endswith((".html", ".htm")):
        processed_data = process_html_file(file_path)
        if processed_data:
            data.append(processed_data)
    elif filename.endswith(".pdf"):
        processed_data = process_pdf_file(file_path)
        if processed_data:
            data.append(processed_data)

# Write the data to a CSV file
output_csv = "output.csv"
csv_columns = ["url", "title", "rating", "content", "tags"]

with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(data)

print(f"Data has been written to {output_csv}")
