import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langdetect import detect
import time

def is_valid_url(url, domain_restrictions):
    """Checks if a URL is valid based on domain restrictions."""
    if not domain_restrictions:
        return True
    return any(urlparse(url).netloc.endswith(domain) for domain in domain_restrictions)

def crawl(seed_urls, domain_restrictions, language, max_pages=50):
    """Crawl the website starting from seed URLs."""
    visited = set()
    queue = list(seed_urls)
    repository = "repository"
    
    # Create a folder for the domain inside repository
    domain_folder = os.path.join(repository, domain_restrictions[0])  # Use domain as folder name
    os.makedirs(domain_folder, exist_ok=True)
    
    report_file = os.path.join(domain_folder, "report.csv")
    
    with open(report_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Number of Outlinks"])
        
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited or not is_valid_url(url, domain_restrictions):
                continue
            
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                text_content = soup.get_text()
                
                if detect(text_content) != language:
                    continue
                
                visited.add(url)
                filename = os.path.join(domain_folder, f"page_{len(visited)}.html")  # Store in domain-specific folder
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                
                outlinks = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
                writer.writerow([url, len(outlinks)])
                queue.extend(outlinks)
                
                time.sleep(1)  # To avoid overloading servers
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")

if __name__ == "__main__":
    domains = [
        #3 different domains each in different languages
        {"seed": ["http://www.retasstudio.net/"], "domain": ["retasstudio.net"], "language": "ja"},
        {"seed": ["https://www.bbc.com"], "domain": ["bbc.com"], "language": "en"},
        {"seed": ["https://elpais.com"], "domain": ["elpais.com"], "language": "es"}
    ]
    
    for domain in domains:
        print(f"Crawling {domain['seed'][0]}...")
        crawl(domain["seed"], domain["domain"], domain["language"])
