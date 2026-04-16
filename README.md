<<<<<<< HEAD
# AUTOCOMPLETION_WITH_COMPRESSED_BURST_TRIE
High-performance autocomplete engine using a Compressed Burst Trie (CBT) with frequency-based ranking, fuzzy search, and a C++ backend integrated with a Python GUI.
=======
# Compressed Burst Trie Autocomplete Engine

A high-performance, memory-efficient autocomplete engine built using C++
(core engine) and a Python GUI (Tkinter).

## Features

-   Lightning-Fast Autocomplete
-   Frequency-Based Ranking
-   Typo-Tolerant Search (Levenshtein Distance ≤ 1)
-   Dynamic Memory Management (Bursting)
-   Persistent Storage
-   Automated Testbench

## How It Works

### Compressed Burst Trie

-   Combines Radix Tree + Burst Trie
-   Uses prefix compression
-   Buckets burst into nodes dynamically

### Ranking

Each word stores frequency: \[word, frequency\]

### Fuzzy Search

Supports edit distance ≤ 1

## 📁 Project Structure

cbt.hpp cbt.cpp main.cpp gui.py testbench.py data.txt saved.txt

## 🛠️ Setup

Compile: g++ -std=c++11 main.cpp cbt.cpp -o autocomplete

Run GUI: python gui.py

Run Testbench: python testbench.py

## 💻 Usage

-   Type prefix → get suggestions
-   Search increases ranking
-   Insert/Delete words
-   Save state to file


## CODE : 
-g++ -std=c++11 main.cpp cbt.cpp -o autocomplete
-python gui.py
-python ./testbench.py
>>>>>>> 64809bb (commit1)
