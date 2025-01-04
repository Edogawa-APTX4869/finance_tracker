# Personal Finance Tracker

## Overview

This is a personal finance tracker web application developed as part of a course project for university, upon request from Mr. Wakil. The system allows users to manage their personal finances efficiently by providing features such as user authentication, secure sign-in and sign-up processes, and a simple interface to track financial activities.

The project was built using Django, Bootstrap, and MongoDB, and is designed to help users keep track of their income, expenses, and savings.

## Main Features

- **User Authentication**: 
  - Users can sign up for an account to store and manage their financial data securely.
  - The system allows users to log in and log out, ensuring that only authorized individuals have access to personal financial information.

- **Responsive Design**:
  - Built using **Bootstrap**, the application has a responsive and user-friendly interface that adapts well to various screen sizes, making it easy to use on both desktops and mobile devices.

- **MongoDB Integration**:
  - The application uses **MongoDB** for storing user data, including login credentials and financial records. This NoSQL database allows for flexible data storage and efficient retrieval.

- **Security**:
  - User credentials are securely stored and processed, ensuring privacy and data protection.

## Technologies Used

- **Django** (Backend): Web framework used for developing the server-side logic.
- **Bootstrap** (Frontend): Used for building a clean and responsive design.
- **MongoDB** (Database): A NoSQL database used to store user data.
- **Python**: The primary programming language for the backend logic.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/finance-tracker.git
   ```
2. Create a virtual environment and activate it with python 3.9:
   ```bash
   python -m venv venv
   ```
3. using the following command in `windows` to activate the virtual environment:
   ```bash
   .\venv\Scripts\activate   

4. Install all Required incandescent from requirements.txt
   ```bash
   pip install -r requirements.txt
    ```
5. Make sure you have MongoDB installed and running on your local machine.
6. Make migrations and migrate the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Run the server:
   ```bash
   python manage.py runserver
   ```

Feel free to check it and reach me anytime.