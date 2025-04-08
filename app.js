// Contact Manager Class
class ContactManager {
    constructor() {
        this.contacts = this.loadContacts();
    }

    loadContacts() {
        const contacts = localStorage.getItem('contacts');
        return contacts ? JSON.parse(contacts) : [];
    }

    saveContacts() {
        localStorage.setItem('contacts', JSON.stringify(this.contacts));
    }

    addContact(contact) {
        this.contacts.push({
            ...contact,
            created_at: new Date().toISOString(),
            last_modified: new Date().toISOString()
        });
        this.saveContacts();
    }

    deleteContact(index) {
        this.contacts.splice(index, 1);
        this.saveContacts();
    }

    searchContacts(query) {
        if (!query) return this.contacts;
        return this.contacts.filter(contact => 
            contact.name.toLowerCase().includes(query.toLowerCase()) ||
            contact.email.toLowerCase().includes(query.toLowerCase()) ||
            contact.phone.includes(query)
        );
    }
}

// Initialize Contact Manager
const contactManager = new ContactManager();

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Index Page
    if (document.getElementById('contactsList')) {
        displayContacts();
        setupSearch();
    }

    // Add Contact Page
    if (document.getElementById('contactForm')) {
        setupAddContactForm();
    }
});

// Display Contacts
function displayContacts(contacts = contactManager.contacts) {
    const contactsList = document.getElementById('contactsList');
    if (!contactsList) return;

    contactsList.innerHTML = contacts.map((contact, index) => `
        <div class="contact-item">
            <div class="contact-info">
                <h5>${contact.name}</h5>
                <p class="mb-1">Age: ${contact.age}</p>
                <p class="mb-1">Email: ${contact.email}</p>
                <p class="mb-0">Phone: ${contact.phone}</p>
            </div>
            <div class="contact-actions">
                <button class="btn btn-danger btn-sm" onclick="deleteContact(${index})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Setup Search
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        const results = contactManager.searchContacts(this.value);
        displayContacts(results);
    });
}

// Setup Add Contact Form
function setupAddContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const contact = {
            name: document.getElementById('name').value.trim(),
            age: parseInt(document.getElementById('age').value),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim()
        };

        // Validate contact
        if (!contact.name || !contact.email || !contact.phone) {
            alert('Please fill in all fields');
            return;
        }

        contactManager.addContact(contact);
        window.location.href = 'index.html';
    });
}

// Delete Contact
function deleteContact(index) {
    if (confirm('Are you sure you want to delete this contact?')) {
        contactManager.deleteContact(index);
        displayContacts();
    }
} 