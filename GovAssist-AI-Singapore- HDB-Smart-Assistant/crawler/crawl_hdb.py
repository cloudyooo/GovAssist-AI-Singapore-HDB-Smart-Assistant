import requests
from bs4 import BeautifulSoup
from database import create_database, save_page, count_pages

# Create database if it doesn't exist
create_database()

URL = "https://www.hdb.gov.sg"

headers = {
    "User-Agent": "GovAssist-AI-Capstone/1.0 (Educational Project)"
}

print("=" * 60)
print("Singapore HDB Smart Assistant")
print("HDB Knowledge Crawler")
print("=" * 60)

print("\nConnecting to HDB...")

try:

    response = requests.get(URL, headers=headers, timeout=15)

    if response.status_code == 200:

        print("✅ Connected successfully.")

        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.get_text(strip=True) if soup.title else "HDB Homepage"

        text = soup.get_text(separator="\n", strip=True)

        save_page(
            source="HDB",
            title=title,
            url=URL,
            content=text
        )

        print(f"Saved page: {title}")

    else:
        print(f"Failed. Status Code: {response.status_code}")

except Exception as e:
    print("Error:", e)

print()
print(f"Total pages stored: {count_pages()}")
