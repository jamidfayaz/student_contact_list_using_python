import json
import os

CONTACT_FILE = "contacts.json"


# ------------------- Utility Functions -------------------

def load_contacts():
    """Load contacts from JSON file."""
    try:
        if not os.path.exists(CONTACT_FILE):
            return []
        with open(CONTACT_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("⚠ Error reading contacts file. Starting fresh.")
        return []
    except Exception as e:
        print(f"⚠ Unexpected error loading contacts: {e}")
        return []


def save_contacts(contacts):
    """Save contacts to JSON file."""
    try:
        with open(CONTACT_FILE, "w") as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print(f"⚠ Error saving contacts: {e}")


def validate_phone(phone):
    return phone.isdigit() and (7 <= len(phone) <= 15)


def validate_email(email):
    return "@" in email and "." in email


# ------------------- Core Features -------------------

def add_contact():
    try:
        name = input("Enter Name: ").strip()
        phone = input("Enter Phone: ").strip()
        email = input("Enter Email: ").strip()

        if not validate_phone(phone):
            raise ValueError("Invalid phone number! Must be 7–15 digits.")

        if not validate_email(email):
            raise ValueError("Invalid email format!")

        contacts = load_contacts()
        contacts.append({"name": name, "phone": phone, "email": email})
        save_contacts(contacts)

        print("✅ Contact added successfully!")

    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")


def view_contacts(sorted_by="name"):
    try:
        contacts = load_contacts()
        if not contacts:
            print("No contacts found.")
            return

        contacts = sorted(contacts, key=lambda x: x[sorted_by])

        print("\n--- Contact List ---")
        for c in contacts:
            print(f"Name: {c['name']} | Phone: {c['phone']} | Email: {c['email']}")
        print("--------------------\n")

    except Exception as e:
        print(f"⚠ Error displaying contacts: {e}")


def search_contact():
    try:
        term = input("Enter name or phone to search: ").strip().lower()
        contacts = load_contacts()

        results = [c for c in contacts if term in c["name"].lower() or term in c["phone"]]

        if results:
            print("\n--- Search Results ---")
            for c in results:
                print(f"Name: {c['name']} | Phone: {c['phone']} | Email: {c['email']}")
            print("----------------------\n")
        else:
            print("❌ No matching contact found.")

    except Exception as e:
        print(f"⚠ Error searching contacts: {e}")


def update_contact():
    try:
        name = input("Enter name of contact to update: ").strip().lower()
        contacts = load_contacts()

        for c in contacts:
            if c["name"].lower() == name:
                print("Leave field empty to keep current value.")

                new_phone = input(f"New Phone ({c['phone']}): ").strip()
                new_email = input(f"New Email ({c['email']}): ").strip()

                if new_phone:
                    if validate_phone(new_phone):
                        c["phone"] = new_phone
                    else:
                        raise ValueError("Invalid phone number!")

                if new_email:
                    if validate_email(new_email):
                        c["email"] = new_email
                    else:
                        raise ValueError("Invalid email format!")

                save_contacts(contacts)
                print("✅ Contact updated successfully!")
                return

        print("❌ Contact not found.")

    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")


def delete_contact():
    try:
        name = input("Enter name of contact to delete: ").strip().lower()
        contacts = load_contacts()

        new_contacts = [c for c in contacts if c["name"].lower() != name]

        if len(new_contacts) == len(contacts):
            print("❌ Contact not found.")
            return

        save_contacts(new_contacts)
        print("🗑 Contact deleted successfully!")

    except Exception as e:
        print(f"⚠ Error deleting contact: {e}")


# ------------------- Menu System -------------------

def menu():
    while True:
        try:
            print("\n====== Smart Contact Book ======")
            print("1. Add Contact")
            print("2. View Contacts")
            print("3. Search Contact")
            print("4. Update Contact")
            print("5. Delete Contact")
            print("6. Exit")
            print("================================")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                add_contact()
            elif choice == "2":
                view_contacts()
            elif choice == "3":
                search_contact()
            elif choice == "4":
                update_contact()
            elif choice == "5":
                delete_contact()
            elif choice == "6":
                print("Exiting Contact Book... Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please try again.")

        except Exception as e:
            print(f"⚠ Menu error: {e}")
            continue


# Run the program
menu()