import os
import collections
import matplotlib.pyplot as plt
import numpy as np

def analyze_heaps_law(stemmed_folder):
    """Analyzes Heap's law by plotting vocabulary size versus collection size."""
    vocab_set = set()
    total_words = 0
    vocab_sizes = []
    word_counts = []

    # Ensure the stemmed_folder exists
    if not os.path.exists(stemmed_folder):
        print(f"Error: The folder {stemmed_folder} does not exist.")
        return

    # Read and process each stemmed file
    for filename in sorted(os.listdir(stemmed_folder)):  # Ensure order of processing
        if filename.endswith("_stemmed.txt"):  # Only process stemmed files
            with open(os.path.join(stemmed_folder, filename), "r", encoding="utf-8") as file:
                words = file.read().split()

                # Process each word in the file
                for word in words:
                    total_words += 1
                    vocab_set.add(word)

                # Track vocabulary size and total word count
                vocab_sizes.append(len(vocab_set))
                word_counts.append(total_words)

    # Plot Heap’s Law
    plt.figure(figsize=(10, 5))
    plt.plot(word_counts, vocab_sizes, marker="o", label="Observed Data")

    # Heap's Law Theoretical Curve
    k = 10  # Empirical constant (tuned for different datasets)
    beta = 0.5  # Common exponent for natural language
    heaps_curve = [k * (n ** beta) for n in word_counts]

    plt.plot(word_counts, heaps_curve, linestyle="dashed", label="Heap’s Law (kN^β)")
    
    # Labeling the axes and adding title
    plt.xlabel("Total Words in Collection (N)")
    plt.ylabel("Vocabulary Size (V)")
    plt.title("Heap’s Law: Vocabulary Growth vs Collection Size")
    plt.legend()
    plt.grid()
    plt.show()

# Run the analysis
stemmed_folder = "stemmed"  # Relative path to the stemmed folder
analyze_heaps_law(stemmed_folder)
