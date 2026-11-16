# Datheon Python Programming Internship

This repository contains four Python projects completed as part of the Datheon Python Programming Internship.

## Projects

### Task 1 – Hangman Game
A command-line word guessing game in which the player guesses a hidden word one letter at a time.

**File:** `Task_1_Hangman/hangman.py`

**Features:**
- Random word selection
- Letter guessing
- Tracks incorrect guesses
- Win and lose conditions

### Task 2 – Stock Portfolio Tracker
A Python application that calculates the value and performance of a stock portfolio using stock price data.

**File:** `Task_2_Stock_Portfolio/portfolio.py`

**Features:**
- Stock ticker validation
- Purchase price and share input
- Investment and current portfolio value calculation
- Profit/loss and return percentage
- CSV summary generation

**Note:** The included stock prices are sample data and are not live market prices.

### Task 3 – Automated File Organizer
A Python utility that organizes files into folders based on their file extensions.

**File:** `Task_3_File_Organizer/organizer.py`

**Features:**
- Automatic file categorization
- Creates category folders
- Handles duplicate filenames
- Logging of file operations
- Handles common file operation errors

### Task 4 – Rule-Based Customer Support Chatbot
An interactive terminal chatbot that recognizes user questions and responds using predefined rules and regular expressions.

**File:** `Task_4_Terminal_Assistant/chatbot.py`

**Features:**
- Greeting recognition
- Business hours and product FAQs
- Price, shipping and payment information
- Return policy responses
- Multiple intent recognition
- Regex-based pattern matching
- Contextual follow-up handling
- Fallback responses
- Exit commands

**Note:** Business hours, delivery details, payment methods and return policy are sample information for demonstration purposes.

## Technologies Used

- Python
- Regular Expressions (`re`)
- CSV file handling
- File and directory operations (`os`, `shutil`, `pathlib`)
- Logging

## Project Structure

 
Datheon_Python_Programming_Internship/
│
├── README.md
├── .gitignore
│
├── Task_1_Hangman/
│   ├── hangman.py
│   └── words.txt
│
├── Task_2_Stock_Portfolio/
│   ├── portfolio.py
│   ├── sp500_tickers.csv
│   ├── stock_prices.csv
│   └── portfolio_summary.csv
│
├── Task_3_File_Organizer/
│   ├── organizer.py
│   └── test_files/
│
└── Task_4_Terminal_Assistant/
    └── chatbot.py
 
## How to Run

Make sure Python is installed on your system.

Open a terminal in the project directory and run the required script.

**Task 1**
 
python Task_1_Hangman/hangman.py
 

**Task 2**
 
python Task_2_Stock_Portfolio/portfolio.py
 

**Task 3**
 
python Task_3_File_Organizer/organizer.py
 

**Task 4**
 
python Task_4_Terminal_Assistant/chatbot.py
 

## Project Status

All four internship tasks have been implemented and tested.

## Author

Completed as part of the Datheon Python Programming Internship.