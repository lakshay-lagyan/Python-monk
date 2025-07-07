import pandas as pd
import numpy as np
import os

class ContactBook:
    def __init__(self, filename="contacts.csv"):
        self.filename = filename
        self.fields = ['Name', 'Phone', 'Email']
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            self.df = pd.read_csv(self.filename)
        else:
            self.df = pd.DataFrame(columns=self.fields)

    def save_contacts(self):
        self.df.to_csv(self.filename, index=False)

    def add_contact(self, name, phone, email):
        if ((self.df['Name'].str.lower() == name.lower()).any()):
            print("Contact already exists.")
            return
        new_contact = pd.DataFrame([[name, phone, email]], columns=self.fields)
        self.df = pd.concat([self.df, new_contact], ignore_index=True)
        self.save_contacts()
        print("Contact added successfully.")

    def list_contacts(self):
        if self.df.empty:
            print("No contacts found.")
        else:
            print(self.df.to_string(index=False))

    def search_contacts(self, keyword):
        results = self.df[self.df['Name'].str.contains(keyword, case=False, na=False)]
        if results.empty:
            print("No contacts found.")
        else:
            print(results.to_string(index=False))

    def delete_contact(self, name):
        idx = self.df[self.df['Name'].str.lower() == name.lower()].index
        if idx.empty:
            print("Contact not found.")
        else:
            self.df = self.df.drop(idx)
            self.save_contacts()
            print("Contact deleted.")

    def analytics(self):
        # Example: Count contacts by email domain
        if self.df.empty:
            print("No contacts to analyze.")
            return
        self.df['Domain'] = self.df['Email'].apply(lambda x: x.split('@')[-1] if '@' in x else np.nan)
        domain_counts = self.df['Domain'].value_counts()
        print("Contacts by Email Domain:")
        print(domain_counts)

def main():
    book = ContactBook()
    menu = """
Contact Book 
1. Add Contact
2. List Contacts
3. Search Contact
4. Delete Contact
5. Analytics
6. Exit
Choice: """
    while True:
        try:
            choice = input(menu).strip()
            if choice == '1':
                name = input("Name: ").strip()
                phone = input("Phone: ").strip()
                email = input("Email: ").strip()
                book.add_contact(name, phone, email)
            elif choice == '2':
                book.list_contacts()
            elif choice == '3':
                keyword = input("Enter name to search: ").strip()
                book.search_contacts(keyword)
            elif choice == '4':
                name = input("Enter name to delete: ").strip()
                book.delete_contact(name)
            elif choice == '5':
                book.analytics()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()