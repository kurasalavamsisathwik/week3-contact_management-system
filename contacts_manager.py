# Contact management system 
# week 3 this is developed using dictionaries
import json
import re
import os
from datetime import datetime

FILE_NAME = "contacts.json"
BACKUP_FILE = "contacts_backup.json"

# -----------------------------
# Helper Validation Functions
# -----------------------------
def validate_name(name):
    name = name.strip()
    return bool(re.match(r"^[A-Za-z ]{2,50}$", name))


def validate_phone(phone):
    phone = phone.strip()
    return bool(re.match(r"^\d{10}$", phone))


def validate_email(email):
    email = email.strip()
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


def clean_string(value):
    return value.strip().title()


# -----------------------------
# File Operations
# -----------------------------
def load_from_file():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            print("⚠ Error reading file. Starting fresh.")
    return {}


def save_to_file(contacts):
    try:
        # Backup before saving
        if os.path.exists(FILE_NAME):
            os.replace(FILE_NAME, BACKUP_FILE)

        with open(FILE_NAME, "w") as file:
            json.dump(contacts, file, indent=4)

    except Exception as e:
        print(f"❌ Error saving file: {e}")


# -----------------------------
# CRUD Operations
# -----------------------------
def add_contact(contacts):
    name = clean_string(input("Enter name: "))

    if not validate_name(name):
        print("❌ Invalid name.")
        return

    if name in contacts:
        print("⚠ Contact already exists.")
        return

    phone = input("Enter phone (10 digits): ")
    if not validate_phone(phone):
        print("❌ Invalid phone number.")
        return

    email = input("Enter email: ")
    if email and not validate_email(email):
        print("❌ Invalid email.")
        return

    address = input("Enter address: ").strip()
    category = input("Enter category (Family/Friends/Work): ").strip()

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address,
        "category": category
    }

    save_to_file(contacts)
    print("✅ Contact added successfully.")


def search_contact(contacts):
    query = input("Enter name or part of name: ").lower()

    results = {
        name: details
        for name, details in contacts.items()
        if query in name.lower()
    }

    if not results:
        print("❌ No matching contacts found.")
        return

    print("\n🔍 Search Results:")
    for name, details in results.items():
        display_contact(name, details)


def search_by_phone(contacts):
    phone_query = input("Enter phone number: ")

    results = {
        name: details
        for name, details in contacts.items()
        if phone_query in details["phone"]
    }

    if not results:
        print("❌ No contacts found.")
        return

    for name, details in results.items():
        display_contact(name, details)


def update_contact(contacts):
    name = clean_string(input("Enter contact name to update: "))

    if name not in contacts:
        print("❌ Contact not found.")
        return

    print("Leave blank to keep existing value.")

    phone = input("New phone: ")
    if phone and not validate_phone(phone):
        print("❌ Invalid phone.")
        return

    email = input("New email: ")
    if email and not validate_email(email):
        print("❌ Invalid email.")
        return

    address = input("New address: ")
    category = input("New category: ")

    if phone:
        contacts[name]["phone"] = phone
    if email:
        contacts[name]["email"] = email
    if address:
        contacts[name]["address"] = address
    if category:
        contacts[name]["category"] = category

    save_to_file(contacts)
    print("✅ Contact updated.")


def delete_contact(contacts):
    name = clean_string(input("Enter contact name to delete: "))

    if name not in contacts:
        print("❌ Contact not found.")
        return

    confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        save_to_file(contacts)
        print("🗑 Contact deleted.")
    else:
        print("❎ Deletion cancelled.")


def display_all(contacts):
    if not contacts:
        print("📭 No contacts available.")
        return

    print("\n📒 All Contacts:")
    for name, details in contacts.items():
        display_contact(name, details)


def display_contact(name, details):
    print(f"""
---------------------------
Name    : {name}
Phone   : {details.get("phone")}
Email   : {details.get("email")}
Address : {details.get("address")}
Category: {details.get("category")}
---------------------------
""")


# -----------------------------
# Advanced Features
# -----------------------------
def export_to_csv(contacts):
    filename = "contacts_export.csv"
    try:
        with open(filename, "w") as file:
            file.write("Name,Phone,Email,Address,Category\n")
            for name, d in contacts.items():
                file.write(f"{name},{d['phone']},{d['email']},{d['address']},{d['category']}\n")

        print(f"✅ Exported to {filename}")
    except Exception as e:
        print(f"❌ Export failed: {e}")


def show_statistics(contacts):
    print("\n📊 Statistics:")
    print(f"Total Contacts: {len(contacts)}")

    categories = {}
    for c in contacts.values():
        cat = c.get("category", "Others")
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in categories.items():
        print(f"{cat}: {count}")


# -----------------------------
# Menu System
# -----------------------------
def menu():
    contacts = load_from_file()

    while True:
        print("""
========= CONTACT MANAGER =========
1. Add Contact
2. Search Contact (Name)
3. Search Contact (Phone)
4. Update Contact
5. Delete Contact
6. Display All Contacts
7. Export to CSV
8. Show Statistics
9. Exit
==================================
""")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_contact(contacts)
            elif choice == "2":
                search_contact(contacts)
            elif choice == "3":
                search_by_phone(contacts)
            elif choice == "4":
                update_contact(contacts)
            elif choice == "5":
                delete_contact(contacts)
            elif choice == "6":
                display_all(contacts)
            elif choice == "7":
                export_to_csv(contacts)
            elif choice == "8":
                show_statistics(contacts)
            elif choice == "9":
                print("👋 Exiting...")
                break
            else:
                print("❌ Invalid choice.")
        except Exception as e:
            print(f"⚠ Unexpected error: {e}")


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    menu()