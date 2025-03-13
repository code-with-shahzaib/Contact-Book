# 📖 Contact Book Manager

A **command-line contact management system** that allows you to **store, update, delete, search, and secure contacts** with a **password-protected system**.  
This project supports **backup, restore, contact categorization, and data validation** to ensure reliability.

---

## 🌟 Features

✅ **Secure Authentication** – Protect contacts with a password.  
✅ **Add Contacts** – Store names, phone numbers, emails, and categories (family, friend, work).  
✅ **Update Contacts** – Modify existing contact details.  
✅ **Delete Contacts** – Remove contacts permanently.  
✅ **Search Contacts** – Find contacts by name, phone, or email.  
✅ **Count Contacts** – View the total number of contacts.  
✅ **View All Contacts** – Display contacts in a table format.  
✅ **Backup & Restore** – Prevent data loss with a backup system.  
✅ **Password Management** – Change your password securely.  
✅ **Data Validation** – Prevents invalid inputs for emails, phone numbers, and ages.  

---

## 🛠 Installation

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/contact-book.git
cd contact-book

2️⃣ Install dependencies
pip install tabulate

3️⃣ Run the script
python contact_book.py

📝 Usage
🔐 First-Time Setup
If the password.txt file is missing, restore it manually or create a new password file.
Contacts are stored in contacts.json in JSON format.

⚡ Example Usage
Adding a Contact
📛 Name: John Doe
📞 Phone: +1234567890
📧 Email: john@example.com
🎂 Age: 28
🏷 Category (family/friend/work): friend
✅ Contact saved!

Searching for a Contact
🔍 Enter search query: John
+----------+-------------+----------------+-----+---------+
| Name     | Phone       | Email          | Age | Category |
+----------+-------------+----------------+-----+---------+
| John Doe | +1234567890 | john@example.com | 28  | friend  |
+----------+-------------+----------------+-----+---------+

🔐 Security Notes
Passwords are hashed using SHA-256 for security.
If you forget the password, delete the password.txt file and reset it manually.

📂 File Structure
📦 contact-book
 ┣ 📜 contact_book.py    # Main Python script
 ┣ 📜 contacts.json      # Stores all contact data (auto-generated)
 ┣ 📜 password.txt       # Stores hashed password (auto-generated)
 ┣ 📜 backup_contacts.json # Backup file
 ┗ 📜 README.md          # Documentation

🚀 Future Enhancements
📅 Add birthday reminders.
🌐 Create a GUI version.
🔗 Sync contacts with online storage.
👨‍💻 Author
Muhammad Shahzaib – Passionate about software development and AI. 🚀
💡 DreamTech Founder | Aspiring AI Developer