# Contact Management System

A simple web-based contact management system built with Python and Flask.

## Features
- Add new contacts
- View all contacts
- Delete contacts
- Search contacts
- Web interface

## Setup Instructions

1. Make sure you have Python installed on your computer
2. Install the required packages:
   ```
   pip install flask
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Project Structure
```
contact_manager/
    ├── app.py              # Flask web application
    ├── project4.py         # Core contact management logic
    ├── contacts.json       # Contact data storage
    └── templates/          # HTML templates
        ├── base.html
        ├── index.html
        └── add.html
```

## Usage
1. View Contacts: Click on "Contacts" in the navigation bar
2. Add Contact: Click "Add Contact" and fill in the details
3. Delete Contact: Click the "Delete" button next to any contact
4. Search: Use the search bar to find contacts by name, email, or phone 