#Contact Management List: Collect User's Name, Age, & Email and store it 
#for loop: for i in range(1,11,2)-> starts at 1, ends at 10, goes in increments of 2
#lists = numbers.append() -> adds number to end of list; numbers.pop(2) removes element from list

import json
import re
from datetime import datetime
import os
from typing import List, Dict, Optional
import csv
from collections import Counter

class ContactManager:
    def __init__(self, file_path: str = "contacts.json"):
        self.file_path = file_path
        self.people = self._load_contacts()

    def _load_contacts(self) -> List[Dict]:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    return json.load(f)["contacts"]
            return []
        except Exception as e:
            print(f"Error loading contacts: {e}")
            return []

    def _save_contacts(self):
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as f:
                json.dump({"contacts": self.people}, f, indent=4)
        except Exception as e:
            print(f"Error saving contacts: {e}")

    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _validate_phone(self, phone: str) -> bool:
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))

    def add_person(self) -> bool:
        try:
            name = input("Name: ").strip()
            if not name:
                print("Name cannot be empty")
                return False

            while True:
                age = input("Age: ").strip()
                try:
                    age = int(age)
                    if age <= 0 or age > 150:
                        print("Please enter a valid age (1-150)")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number for age")

            while True:
                email = input("Email: ").strip()
                if self._validate_email(email):
                    break
                print("Please enter a valid email address")

            phone = input("Phone (optional): ").strip()
            if phone and not self._validate_phone(phone):
                print("Invalid phone number format")
                return False

            category = input("Category (optional): ").strip()
            
            # Add birthday field
            birthday = input("Birthday (DD/MM/YYYY) (optional): ").strip()
            
            person = {
                "name": name,
                "age": age,
                "email": email,
                "phone": phone,
                "category": category,
                "birthday": birthday,
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
            
            self.people.append(person)
            self._save_contacts()
            print("Person added successfully!")
            return True
        except Exception as e:
            print(f"Error adding person: {e}")
            return False

    def edit_person(self):
        self.display_people(self.people)
        while True:
            try:
                number = int(input("Enter the number of the person to edit: "))
                if 1 <= number <= len(self.people):
                    person = self.people[number - 1]
                    print("\nCurrent details:")
                    self.display_person(person)
                    
                    print("\nEnter new details (press Enter to keep current value):")
                    name = input(f"Name [{person['name']}]: ").strip() or person['name']
                    
                    while True:
                        age_input = input(f"Age [{person['age']}]: ").strip()
                        if not age_input:
                            age = person['age']
                            break
                        try:
                            age = int(age_input)
                            if age <= 0 or age > 150:
                                print("Please enter a valid age (1-150)")
                            else:
                                break
                        except ValueError:
                            print("Please enter a valid number for age")

                    while True:
                        email = input(f"Email [{person['email']}]: ").strip() or person['email']
                        if self._validate_email(email):
                            break
                        print("Please enter a valid email address")

                    phone = input(f"Phone [{person['phone']}]: ").strip() or person['phone']
                    if phone and not self._validate_phone(phone):
                        print("Invalid phone number format")
                        return

                    category = input(f"Category [{person['category']}]: ").strip() or person['category']

                    person.update({
                        "name": name,
                        "age": age,
                        "email": email,
                        "phone": phone,
                        "category": category,
                        "last_modified": datetime.now().isoformat()
                    })
                    
                    self._save_contacts()
                    print("Person updated successfully!")
                    return
                else:
                    print("Invalid number")
            except ValueError:
                print("Please enter a valid number")

    def delete_person(self):
        self.display_people(self.people)
        while True:
            try:
                number = int(input("Enter the number of the person to delete: "))
                if 1 <= number <= len(self.people):
                    person = self.people.pop(number - 1)
                    self._save_contacts()
                    print(f"Deleted: {person['name']}")
                    return
                else:
                    print("Invalid number")
            except ValueError:
                print("Please enter a valid number")

    def search(self):
        print("\nSearch by:")
        print("1. Name")
        print("2. Email")
        print("3. Phone")
        print("4. Category")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-4): "))
                if 1 <= choice <= 4:
                    break
                print("Please enter a number between 1 and 4")
            except ValueError:
                print("Please enter a valid number")

        search_term = input("Enter search term: ").strip().lower()
        results = []

        for person in self.people:
            if choice == 1 and search_term in person["name"].lower():
                results.append(person)
            elif choice == 2 and search_term in person["email"].lower():
                results.append(person)
            elif choice == 3 and search_term in person["phone"].lower():
                results.append(person)
            elif choice == 4 and search_term in person["category"].lower():
                results.append(person)

        if results:
            print("\nSearch Results:")
            self.display_people(results)
        else:
            print("No results found")

    def display_person(self, person: Dict):
        print(f"Name: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"Email: {person['email']}")
        print(f"Phone: {person['phone']}")
        print(f"Category: {person['category']}")
        print(f"Last Modified: {person['last_modified']}")

    def display_people(self, people: List[Dict]):
        if not people:
            print("No contacts found")
            return

        print("\nContacts:")
        print("-" * 80)
        print(f"{'No.':<5} {'Name':<20} {'Age':<5} {'Email':<30} {'Phone':<15} {'Category':<15}")
        print("-" * 80)
        
        for i, person in enumerate(people, 1):
            print(f"{i:<5} {person['name'][:20]:<20} {person['age']:<5} "
                  f"{person['email'][:30]:<30} {person['phone'][:15]:<15} "
                  f"{person['category'][:15]:<15}")
        print("-" * 80)

    def sort_contacts(self):
        print("\nSort by:")
        print("1. Name")
        print("2. Age")
        print("3. Category")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if 1 <= choice <= 3:
                    break
                print("Please enter a number between 1 and 3")
            except ValueError:
                print("Please enter a valid number")

        reverse = input("Sort in descending order? (y/n): ").lower() == 'y'
        
        if choice == 1:
            self.people.sort(key=lambda x: x['name'].lower(), reverse=reverse)
        elif choice == 2:
            self.people.sort(key=lambda x: x['age'], reverse=reverse)
        else:
            self.people.sort(key=lambda x: x['category'].lower(), reverse=reverse)
        
        self._save_contacts()
        print("\nSorted contacts:")
        self.display_people(self.people)

    def show_statistics(self):
        """Display basic statistics about contacts"""
        if not self.people:
            print("No contacts to analyze")
            return

        # Count contacts by category
        categories = [person['category'] for person in self.people if person['category']]
        category_counts = Counter(categories)
        
        # Calculate average age
        ages = [person['age'] for person in self.people]
        avg_age = sum(ages) / len(ages)
        
        print("\nContact Statistics:")
        print("-" * 40)
        print(f"Total Contacts: {len(self.people)}")
        print(f"Average Age: {avg_age:.1f}")
        
        if category_counts:
            print("\nContacts by Category:")
            for category, count in category_counts.items():
                print(f"{category}: {count}")
        
        # Show upcoming birthdays
        print("\nUpcoming Birthdays (next 30 days):")
        today = datetime.now()
        for person in self.people:
            if person.get('birthday'):
                try:
                    birthday = datetime.strptime(person['birthday'], '%d/%m/%Y')
                    # Calculate days until birthday
                    next_birthday = birthday.replace(year=today.year)
                    if next_birthday < today:
                        next_birthday = next_birthday.replace(year=today.year + 1)
                    days_until = (next_birthday - today).days
                    if 0 <= days_until <= 30:
                        print(f"{person['name']}: {days_until} days until birthday")
                except ValueError:
                    continue

    def export_to_csv(self):
        """Export contacts to a CSV file"""
        if not self.people:
            print("No contacts to export")
            return

        filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Define the fields to export
                fieldnames = ['name', 'age', 'email', 'phone', 'category', 'birthday']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for person in self.people:
                    # Only write the fields we want to export
                    export_data = {field: person.get(field, '') for field in fieldnames}
                    writer.writerow(export_data)
            
            print(f"\nContacts exported successfully to {filename}")
        except Exception as e:
            print(f"Error exporting contacts: {e}")

def main():
    print("Welcome to the Enhanced Contact Management System")
    print("=" * 50)
    
    contact_manager = ContactManager()
    
    while True:
        print("\nAvailable Commands:")
        print("1. Add Contact")
        print("2. Edit Contact")
        print("3. Delete Contact")
        print("4. Search Contacts")
        print("5. Sort Contacts")
        print("6. Display All Contacts")
        print("7. Show Statistics")
        print("8. Export to CSV")
        print("9. Quit")
        
        command = input("\nEnter your choice (1-9): ").strip()
        
        if command == "1":
            contact_manager.add_person()
        elif command == "2":
            contact_manager.edit_person()
        elif command == "3":
            contact_manager.delete_person()
        elif command == "4":
            contact_manager.search()
        elif command == "5":
            contact_manager.sort_contacts()
        elif command == "6":
            contact_manager.display_people(contact_manager.people)
        elif command == "7":
            contact_manager.show_statistics()
        elif command == "8":
            contact_manager.export_to_csv()
        elif command == "9":
            print("Thank you for using the Contact Management System!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

