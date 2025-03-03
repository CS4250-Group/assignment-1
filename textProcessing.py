import os
import re
import csv
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from collections import Counter
import nltk
from langdetect import detect, DetectorFactory

nltk.download('punkt')

# Ensure language detection is deterministic
DetectorFactory.seed = 0

def detect_language(text):
    """Detect the language of the given text safely."""
    try:
        return detect(text)
    except:
        return "unknown"

def tokenize_and_stem():
    """Tokenize and apply stemming to crawled documents and classify by language."""
    repository = "repository"
    tokenized_folder = "tokenized"
    stemmed_folder = "stemmed"
    os.makedirs(tokenized_folder, exist_ok=True)
    os.makedirs(stemmed_folder, exist_ok=True)

    stemmer = PorterStemmer()

    # Dictionary to store frequency per language category
    crawl_stem_frequencies = {
        "english": Counter(),
        "french": Counter(),
        "spanish": Counter()
    }

    # Sort files to maintain order
    files = sorted(os.listdir(repository))

    for file in files:
        if file.endswith(".html"):
            with open(os.path.join(repository, file), "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                text = soup.get_text().strip()

                if not text:
                    continue  # Skip empty files

                # Detect language
                lang = detect_language(text)
                if lang.startswith("en"):
                    category = "english"
                elif lang.startswith("fr"):
                    category = "french"
                elif lang.startswith("es"):
                    category = "spanish"
                else:
                    continue  # Skip if language is unknown

                # Tokenization: Keep only alphanumeric words
                tokens = re.findall(r'\b\w+\b', text.lower())

                # Stemming
                stemmed_tokens = [stemmer.stem(word) for word in tokens]

                # Update corresponding language category
                crawl_stem_frequencies[category].update(stemmed_tokens)

                # Save tokenized and stemmed versions
                tokenized_filename = os.path.join(tokenized_folder, file.replace(".html", "_tokenized.txt"))
                with open(tokenized_filename, "w", encoding="utf-8") as tf:
                    tf.write(" ".join(tokens))

                stemmed_filename = os.path.join(stemmed_folder, file.replace(".html", "_stemmed.txt"))
                with open(stemmed_filename, "w", encoding="utf-8") as sf:
                    sf.write(" ".join(stemmed_tokens))

    return crawl_stem_frequencies

def save_top_stems(crawl_stem_frequencies, report_filename):
    """Save the top 50 most frequent stems to a CSV file."""
    most_common_stems = crawl_stem_frequencies.most_common(50)

    with open(report_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Stem", "Frequency"])
        for stem, frequency in most_common_stems:
            writer.writerow([stem, frequency])

if __name__ == "__main__":
    print("Processing tokenization, stemming, and generating word frequency reports...")

    crawl_stem_frequencies = tokenize_and_stem()

    save_top_stems(crawl_stem_frequencies["english"], "repository/Words1.csv")  # English
    save_top_stems(crawl_stem_frequencies["french"], "repository/Words2.csv")   # French
    save_top_stems(crawl_stem_frequencies["spanish"], "repository/Words3.csv")  # Spanish

    print("Tokenization, stemming, and word frequency reports complete.")
