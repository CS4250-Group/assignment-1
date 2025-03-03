import os
import csv
from collections import Counter
import re
import matplotlib.pyplot as plt

def analyze_zipfs_law(stemmed_folder):
    """Analyzes Zipf's law by checking the frequencies and ranks of words."""
    word_frequencies = []

    # Ensure stemmed_folder exists
    if not os.path.exists(stemmed_folder):
        print(f"Error: The folder {stemmed_folder} does not exist.")
        return

    # Loop through files in the stemmed folder
    for filename in os.listdir(stemmed_folder):
        if filename.endswith("_stemmed.txt"):  # Ensure we're only processing stemmed files
            with open(os.path.join(stemmed_folder, filename), "r", encoding="utf-8") as f:
                text = f.read()
                words = re.findall(r'\b\w+\b', text.lower())  # Tokenize into words
                word_frequencies.extend(words)

    # Count word frequencies
    word_counts = Counter(word_frequencies)
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Get word frequencies and ranks
    frequencies = [count for word, count in sorted_word_counts]
    ranks = list(range(1, len(frequencies) + 1))

    # Plot Zipf's Law analysis
    plt.figure(figsize=(10, 6))
    plt.plot(ranks, frequencies, marker='o')
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.title("Zipf's Law Analysis")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    stemmed_folder = "stemmed"  # Relative path to the stemmed folder
    analyze_zipfs_law(stemmed_folder)
