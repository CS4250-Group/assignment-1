import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langdetect import detect
import time

def is_valid_url(url, domain_restrictions):
    if not domain_restrictions:
        return True
    return any(urlparse(url).netloc.endswith(domain) for domain in domain_restrictions)

def crawl(seed_urls, domain_restrictions, language, report_filename, seed_index, max_pages=50):
    visited = set()
    queue = list(seed_urls)
    repository = "repository"
    os.makedirs(repository, exist_ok=True)
    
    report_file_path = os.path.join(repository, report_filename)
    
    with open(report_file_path, "w", newline="", encoding="utf-8") as file:
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
                # Modify filename to include the seed index, ensuring no overwriting
                filename = os.path.join(repository, f"page_{seed_index}_{len(visited)}.html")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                
                outlinks = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
                writer.writerow([url, len(outlinks)])
                queue.extend(outlinks)
                
                time.sleep(1) 
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")

if __name__ == "__main__":
    domains = [
        # 3 different domains each in different languages
        {"seed": ["https://www.bbc.com/news"], "domain": ["bbc.com"], "language": "en", "report_filename": "Report1.csv"},
        {"seed": ["https://www.lemonde.fr"], "domain": ["lemonde.fr"], "language": "fr", "report_filename": "Report2.csv"},
        {"seed": ["https://elpais.com/us"], "domain": ["elpais.com"], "language": "es", "report_filename": "Report3.csv"}
    ]
    
    # Start crawling for each domain
    for idx, domain in enumerate(domains, start=1):
        print(f"Crawling {domain['seed'][0]}...")
        crawl(domain["seed"], domain["domain"], domain["language"], domain["report_filename"], seed_index=idx)
