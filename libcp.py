import json
from datetime import datetime

FILE_PATH = "library.json"


# ---------------- FILE HANDLING ----------------
def load_data():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        data = {
            "books": {
                "101": {"title": "Python Basics", "available": True},
                "102": {"title": "Data Structures", "available": True},
                "103": {"title": "Machine Learning", "available": True}
            },
            "issued": {}
        }
        save_data(data)
        return data


def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


# ---------------- LIBRARY FUNCTIONS ----------------
def display_books():
    data = load_data()
    print("\n📚 Available Books:")

    for book_id, info in data["books"].items():
        status = "Available" if info["available"] else "Issued"
        print(f"ID: {book_id} | {info['title']} | {status}")


def issue_book():
    data = load_data()
    book_id = input("Enter Book ID to issue: ")

    if book_id not in data["books"]:
        print("❌ Book not found!")
        return

    if not data["books"][book_id]["available"]:
        print("❌ Book already issued!")
        return

    name = input("Enter student name: ")
    duration = int(input("Enter duration (in days): "))
    issue_date = datetime.now().strftime("%d-%m-%Y")

    data["books"][book_id]["available"] = False
    data["issued"][book_id] = {
        "name": name,
        "issue_date": issue_date,
        "duration": duration
    }

    save_data(data)
    print("✅ Book issued successfully!")


def return_book():
    data = load_data()
    book_id = input("Enter Book ID to return: ")

    if book_id not in data["issued"]:
        print("❌ This book was not issued!")
        return

    issue_info = data["issued"][book_id]

    issue_date = datetime.strptime(issue_info["issue_date"], "%d-%m-%Y")
    duration = issue_info["duration"]
    return_date = datetime.now()

    days_used = (return_date - issue_date).days
    late_days = days_used - duration

    fine = calculate_fine(late_days)

    print(f"\n📄 Book returned by: {issue_info['name']}")
    print(f"Days used: {days_used}")
    if fine > 0:
        print(f"💰 Fine to pay: ₹{fine}")
    else:
        print("✅ No fine!")

    # Update records
    data["books"][book_id]["available"] = True
    del data["issued"][book_id]

    save_data(data)


def calculate_fine(late_days):
    if late_days <= 0:
        return 0

    # Progressive fine: ₹10 per week
    weeks = (late_days // 7) + 1
    return weeks * 10


def show_issued_books():
    data = load_data()
    print("\n📖 Issued Books:")

    if not data["issued"]:
        print("No books issued.")
        return

    for book_id, info in data["issued"].items():
        print(f"ID: {book_id} | Name: {info['name']} | Date: {info['issue_date']} | Duration: {info['duration']} days")


# ---------------- MAIN MENU ----------------
def library_menu():
    while True:
        print("\n===== LIBRARY MENU =====")
        print("1. Display Books")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Show Issued Books")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            display_books()
        elif choice == "2":
            issue_book()
        elif choice == "3":
            return_book()
        elif choice == "4":
            show_issued_books()
        elif choice == "5":
            print("👋 Exiting Library System!")
            break
        else:
            print("❌ Invalid choice!")


# ---------------- RUN ----------------
if __name__ == "__main__":
    library_menu()
