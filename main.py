import json
import os
import hashlib
import re
from typing import Dict
from tabulate import tabulate  

# 📁 Configuration
CONTACTS_FILE = "contacts.json"
PASSWORD_FILE = "password.txt"
VALID_CATEGORIES = {"family", "friend", "work"}

# 🔧 Utilities
def wait_for_enter() -> None:
    """Pause execution until Enter is pressed."""
    input("\nPress Enter to continue...")

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validate email format using regex."""
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    return re.match(r"^\+?[0-9\s-]{7,}$", phone) is not None

# 🔐 Authentication
def authenticate() -> bool:
    """Authenticate user with password (3 attempts allowed)."""
    if not os.path.exists(PASSWORD_FILE):
        exit("🚨 Security Warning: Password file missing! Restore it manually.")

    with open(PASSWORD_FILE) as f:
        stored_hash = f.read().strip()

    for attempt in range(3, 0, -1):
        if hash_password(input("🔑 Enter password: ").strip()) == stored_hash:
            print("✅ Access Granted!")
            return True
        print(f"❌ Incorrect! {attempt-1} attempts left.")

    exit("🚨 Too many failed attempts!")

def change_password() -> None:
    """Change the stored password after verification."""
    with open(PASSWORD_FILE) as f:
        current_hash = f.read().strip()

    if hash_password(input("🔒 Current password: ").strip()) != current_hash:
        print("❌ Incorrect password!")
        return

    new_pass = input("🆕 New password: ").strip()
    if new_pass != input("🔄 Confirm password: ").strip():
        print("❌ Passwords don't match!")
        return

    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(new_pass))
    print("✅ Password changed!")

# 📇 Contact Management
def load_contacts() -> Dict[str, dict]:
    """Load contacts safely; reset only with confirmation if corrupted."""
    try:
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE) as f:
                return {contact["name"]: contact for contact in json.load(f)}
        return {}
    except (json.JSONDecodeError, KeyError):
        print("⚠ Error loading contacts! File may be corrupted.")
        if input("🔄 Reset contacts file? (y/n): ").strip().lower() == "y":
            return {}
        exit("❌ Exiting to prevent data loss!")

def save_contacts(contacts: Dict[str, dict]) -> None:
    """Save contacts dictionary to file."""
    with open(CONTACTS_FILE, "w") as f:
        json.dump(list(contacts.values()), f, indent=4)

def get_valid_age() -> int:
    """Get and validate age input."""
    while True:
        try:
            return int(input("🎂 Age: ").strip())
        except ValueError:
            print("❌ Invalid age!")

def get_valid_category() -> str:
    """Get and validate contact category."""
    while True:
        category = input(f"🏷 Category ({'/'.join(VALID_CATEGORIES)}): ").strip().lower()
        if category in VALID_CATEGORIES:
            return category
        print("❌ Invalid category!")

def store_contact() -> None:
    """Add a new contact with validation."""
    contacts = load_contacts()
    
    while True:
        name = input("📛 Name: ").strip().lower()
        if not name:
            print("❌ Name cannot be empty!")
        elif name in contacts:
            print("❌ Name exists!")
        else:
            break

    while True:
        phone = input("📞 Phone: ").strip()
        if validate_phone(phone):
            break
        print("❌ Invalid phone format!")

    while True:
        email = input("📧 Email: ").strip().lower()
        if validate_email(email):
            break
        print("❌ Invalid email!")

    contacts[name] = {
        "name": name,
        "phone_number": phone,
        "email": email,
        "age": get_valid_age(),
        "category": get_valid_category()
    }
    
    save_contacts(contacts)
    print("✅ Contact saved!")
    wait_for_enter()

def update_contact() -> None:
    """Update contact details, including renaming the contact."""
    contacts = load_contacts()
    old_name = input("🔍 Name to update: ").strip().lower()

    if old_name not in contacts:
        print("❌ Contact not found!")
        wait_for_enter()
        return

    contact = contacts.pop(old_name)
    print("\nLeave blank to keep current value:")

    new_name = input(f"📛 New name ({old_name}): ").strip().lower() or old_name
    if new_name in contacts:
        print("❌ A contact with this name already exists!")
        contacts[old_name] = contact  # Restore original
        wait_for_enter()
        return

    contact["name"] = new_name
    contact["phone_number"] = input(f"📞 Phone ({contact['phone_number']}): ").strip() or contact["phone_number"]
    contact["email"] = input(f"📧 Email ({contact['email']}): ").strip().lower() or contact["email"]
    contact["age"] = get_valid_age()
    contact["category"] = get_valid_category()

    contacts[new_name] = contact
    save_contacts(contacts)
    print("✅ Contact updated!")
    wait_for_enter()

def delete_contact() -> None:
    """Delete a contact by name."""
    contacts = load_contacts()
    name = input("🗑 Name to delete: ").strip().lower()
    
    if contacts.pop(name, None):
        save_contacts(contacts)
        print("✅ Contact deleted!")
    else:
        print("❌ Contact not found!")
    wait_for_enter()

def search_contact() -> None:
    """Search for a contact by name, phone, or email."""
    contacts = load_contacts()
    query = input("🔍 Enter search query (name, phone, or email): ").strip().lower()

    results = [c for c in contacts.values() if query in c["name"] or query in c["phone_number"] or query in c["email"]]

    if results:
        print(tabulate(results, headers="keys", tablefmt="grid"))
    else:
        print("❌ No matches found!")
    wait_for_enter()

def view_all() -> None:
    """Display all contacts in a table."""
    contacts = load_contacts().values()
    
    if contacts:
        print(tabulate(contacts, headers="keys", tablefmt="grid"))
    else:
        print("📭 No contacts found!")
    wait_for_enter()

def count_contacts() -> None:
    """Show total number of contacts."""
    print(f"\n📊 Total contacts: {len(load_contacts())}")
    wait_for_enter()

def backup_contacts() -> None:
    """Creates a backup of the contacts file."""
    if not os.path.exists(CONTACTS_FILE):
        print("❌ No contacts to back up!")
        return
    os.rename(CONTACTS_FILE, f"backup_{CONTACTS_FILE}")
    print("✅ Backup created!")

def restore_contacts() -> None:
    """Restores contacts from the last backup."""
    if os.path.exists(f"backup_{CONTACTS_FILE}"):
        os.rename(f"backup_{CONTACTS_FILE}", CONTACTS_FILE)
        print("✅ Contacts restored from backup!")
    else:
        print("❌ No backup found!")

# 🚀 Main Application
def main() -> None:
    print("\n----------- 📖 Contact Book Manager 📖 -----------")
    authenticate()

    menu = {
        '1': ("Add Contact", store_contact),
        '2': ("Update Contact", update_contact),
        '3': ("Delete Contact", delete_contact),
        '4': ("Search Contacts", search_contact),
        '5': ("Count Contacts", count_contacts),
        '6': ("Change Password", change_password),
        '7': ("View All", view_all),
        '8': ("Backup Contacts", backup_contacts),
        '9': ("Restore Contacts", restore_contacts),
        '0': ("Exit", exit)
    }

    while True:
        print("\n📌 Menu:")
        for key, (text, _) in menu.items():
            print(f"{key}️⃣  {text}")
        
        menu.get(input("\n➡ Your choice: ").strip(), (None, lambda: print("⚠ Invalid choice!")))[1]()

if __name__ == "__main__":
    main()
