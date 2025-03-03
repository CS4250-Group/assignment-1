import os
import re
import csv
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
from collections import Counter

nltk.download('punkt')

def tokenize_and_stem():
    """Tokenize and apply stemming to crawled documents."""
    repository = "repository"
    tokenized_folder = "tokenized"
    stemmed_folder = "stemmed"
    os.makedirs(tokenized_folder, exist_ok=True)
    os.makedirs(stemmed_folder, exist_ok=True)

    stemmer = PorterStemmer()

    # Loop over each domain folder in the repository
    for domain_folder in os.listdir(repository):
        domain_folder_path = os.path.join(repository, domain_folder)
        
        if os.path.isdir(domain_folder_path):  # Check if it's a directory (domain folder)
            # Process HTML files inside each domain folder
            crawl_stem_frequencies = Counter()
            for file in os.listdir(domain_folder_path):
                if file.endswith(".html"):
                    with open(os.path.join(domain_folder_path, file), "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f.read(), "html.parser")
                        text = soup.get_text()

                        # Tokenization: Keep only alphanumeric words
                        tokens = re.findall(r'\b\w+\b', text.lower())

                        # Save tokenized text
                        tokenized_filename = os.path.join(tokenized_folder, domain_folder + "_" + file.replace(".html", "_tokenized.txt"))
                        with open(tokenized_filename, "w", encoding="utf-8") as tf:
                            tf.write(" ".join(tokens))

                        # Stemming
                        stemmed_tokens = [stemmer.stem(word) for word in tokens]

                        # Save stemmed text
                        stemmed_filename = os.path.join(stemmed_folder, domain_folder + "_" + file.replace(".html", "_stemmed.txt"))
                        with open(stemmed_filename, "w", encoding="utf-8") as sf:
                            sf.write(" ".join(stemmed_tokens))

                        # Update stem frequency count for the domain
                        crawl_stem_frequencies.update(stemmed_tokens)

            # Ensure the directory for Words.csv exists
            words_csv_filename = os.path.join(domain_folder_path, "Words.csv")
            os.makedirs(domain_folder_path, exist_ok=True)  # Ensure the domain folder exists before writing CSV

            # Save top 50 most common stems for each domain in Words.csv
            with open(words_csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Stem", "Frequency"])
                for stem, frequency in crawl_stem_frequencies.most_common(50):
                    writer.writerow([stem, frequency])

if __name__ == "__main__":
    print("Processing tokenization and stemming...")
    tokenize_and_stem()
    print("Tokenization and stemming complete.")
