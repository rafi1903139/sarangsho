# Sarangsho

This is a book review website developed using Django. The website allows users to review and rate books, search books by categories, and more.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)


## Features

- User registration and authentication.
- Users can search for books and view book details.
- Users can write reviews and rate books.
- Users can add books to their reading list.
- Admin panel for managing books, reviews, and users.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (>=3.10) and pip installed.
- Django (>=4.2) installed.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/book-review-website.git


2. **Create a virtual environment and activate it:**

   ```bash
     python3 -m venv venv
     source venv/bin/activate

3. **Install project dependencies:**

   ```bash
     pip install -r requirements.txt
   
4. **Apply database migrations:**

   ```bash
     python manage.py migrate

5. **Create superuser for admin panel:**

   ```bash
     python manage.py createsuperuser

6. **Start the development server:**

   ```bash
     python manage.py runserver

The website should now be accessible at http://localhost:8000/.

## Usage
1. Register a user account or log in.
2. Explore the website, search for books, and read/write reviews.
3. Track your reading progress.
4. Access the admin panel at http://localhost:8000/admin/ using the superuser credentials to manage books, reviews, and users.
 








