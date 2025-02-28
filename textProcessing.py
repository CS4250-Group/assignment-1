import os
import re
import csv
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
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

    #storing the frequency of stems per crawl
    crawl_stem_frequencies = []

    for idx, file in enumerate(os.listdir(repository), start=1):
        if file.endswith(".html"):
            with open(os.path.join(repository, file), "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                text = soup.get_text()

                #tokenization: Keep only alphanumeric words
                tokens = re.findall(r'\b\w+\b', text.lower())

                #stemming
                stemmed_tokens = [stemmer.stem(word) for word in tokens]

                stem_frequencies = Counter(stemmed_tokens)
                
                crawl_stem_frequencies.append(stem_frequencies)

                tokenized_filename = os.path.join(tokenized_folder, file.replace(".html", "_tokenized.txt"))
                with open(tokenized_filename, "w", encoding="utf-8") as tf:
                    tf.write(" ".join(tokens))

                stemmed_filename = os.path.join(stemmed_folder, file.replace(".html", "_stemmed.txt"))
                with open(stemmed_filename, "w", encoding="utf-8") as sf:
                    sf.write(" ".join(stemmed_tokens))

    return crawl_stem_frequencies

def save_top_stems(crawl_stem_frequencies, report_filename):
    """Save the top 50 most frequent stems to a CSV file."""
    all_stems = Counter()

    for stem_frequencies in crawl_stem_frequencies:
        all_stems.update(stem_frequencies)
    
    most_common_stems = all_stems.most_common(50)
    
    with open(report_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Stem", "Frequency"])
        for stem, frequency in most_common_stems:
            writer.writerow([stem, frequency])

if __name__ == "__main__":
    print("Processing tokenization, stemming, and generating word frequency reports...")

    crawl_stem_frequencies = tokenize_and_stem()

    save_top_stems(crawl_stem_frequencies[:1], "repository/Words1.csv")
    save_top_stems(crawl_stem_frequencies[1:2], "repository/Words2.csv")
    save_top_stems(crawl_stem_frequencies[2:3], "repository/Words3.csv")

    print("Tokenization, stemming, and word frequency reports complete.")
