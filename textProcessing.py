import os
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')

def tokenize_and_stem():
    """Tokenize and apply stemming to crawled documents."""
    repository = "repository"
    tokenized_folder = "tokenized"
    stemmed_folder = "stemmed"
    os.makedirs(tokenized_folder, exist_ok=True)
    os.makedirs(stemmed_folder, exist_ok=True)

    stemmer = PorterStemmer()

    for file in os.listdir(repository):
        if file.endswith(".html"):
            with open(os.path.join(repository, file), "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                text = soup.get_text()

                # Tokenization: Keep only alphanumeric words
                tokens = re.findall(r'\b\w+\b', text.lower())

                # Save tokenized text
                tokenized_filename = os.path.join(tokenized_folder, file.replace(".html", "_tokenized.txt"))
                with open(tokenized_filename, "w", encoding="utf-8") as tf:
                    tf.write(" ".join(tokens))

                # Stemming
                stemmed_tokens = [stemmer.stem(word) for word in tokens]

                # Save stemmed text
                stemmed_filename = os.path.join(stemmed_folder, file.replace(".html", "_stemmed.txt"))
                with open(stemmed_filename, "w", encoding="utf-8") as sf:
                    sf.write(" ".join(stemmed_tokens))

if __name__ == "__main__":
    print("Processing tokenization and stemming...")
    tokenize_and_stem()
    print("Tokenization and stemming complete.")
