from flask import Flask, render_template, request, redirect, url_for, flash
from project4 import ContactManager
from datetime import datetime
import os

# Create Flask application
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Initialize contact manager with absolute path
contact_manager = ContactManager(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contacts.json'))

@app.route('/')
def index():
    return render_template('index.html', contacts=contact_manager.people)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            age = int(request.form['age'])
            email = request.form['email'].strip()
            phone = request.form['phone'].strip()

            person = {
                "name": name,
                "age": age,
                "email": email,
                "phone": phone,
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
            
            contact_manager.people.append(person)
            contact_manager._save_contacts()
            flash('Contact added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding contact: {str(e)}', 'error')
    
    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete_contact(index):
    try:
        if 0 <= index < len(contact_manager.people):
            contact_manager.people.pop(index)
            contact_manager._save_contacts()
            flash('Contact deleted successfully!', 'success')
        else:
            flash('Invalid contact index', 'error')
    except Exception as e:
        flash(f'Error deleting contact: {str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/search')
def search_contacts():
    query = request.args.get('q', '').lower()
    if query:
        results = [
            person for person in contact_manager.people
            if query in person['name'].lower() or
               query in person['email'].lower() or
               query in person['phone'].lower()
        ]
    else:
        results = contact_manager.people
    return render_template('index.html', contacts=results, search_query=query)

# This is important for PythonAnywhere
if __name__ == '__main__':
    app.run(debug=True) 