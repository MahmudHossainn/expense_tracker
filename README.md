# Expense Tracker Web App

A simple and user-friendly web application to track your expenses, visualize spending patterns, and manage budgets. This app supports segregating expenses by using user accounts.

## Features

User authentication (registration and login).

Add, view, and categorize expenses.

Generate reports with pie charts to visualize spending.

Responsive and intuitive user interface.

Persistent data storage using SQLite.

## Website Link

The website can be accessed by using the following link: [Expense Tracker](https://mahmud076.pythonanywhere.com/).

## Host Locally

The web app can be hosted locally by using the instructions below.

## Prerequisites

1. Python 3.x installed on your system.

2. pip (Python package installer).

## Setup Instructions

### Step 1: Clone the Repository

Use Git to clone the repository:

    git clone https://github.com/your-username/expense-tracker.git
    
### Step 2: Set Up a Virtual Environment

**Windows:**

Open Command Prompt and navigate to the project folder:

    cd expense-tracker

Create a virtual environment:

    python -m venv venv

Activate the virtual environment:

    venv\Scripts\activate

**MacOS/Linux:**

Open a terminal and navigate to the project folder:

    cd expense-tracker
    
Create a virtual environment:

    python3 -m venv venv

Activate the virtual environment:

    source venv/bin/activate
    
### Step 3: Install Dependencies

Install the required packages using pip:

    pip install -r requirements.txt
    
### Step 4: Initialize the Database

Run the following commands to create the SQLite database and its tables:

    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    
### Step 5: Run the Application

Start the Flask development server:

    python app.py
    
The app will be accessible at http://127.0.0.1:5000 in your browser.

## How to Use

**Register:** Create a new account.

**Login:** Access your personalized expense tracker.

**Add Expenses:** Enter your daily expenses with categories.

**View Reports:** Generate and view spending reports.

