import json
import os
import re
from crypto_utils import encrypt, decrypt, derive_key, generate_password

DB_FILE = "storage.json"

def validate_master_password(pwd: str) -> bool:
    if len(pwd) < 10:
        return False
    if not re.search(r"[A-Z]", pwd):
        return False
    if not re.search(r"[a-z]", pwd):
        return False
    if not re.search(r"[0-9]", pwd):
        return False
    if not re.search(r"[^A-Za-z0-9]", pwd):
        return False
    return True

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def main():
    print("=== Simple Password Manager ===")
    master = input("Enter master password: ")

    if not validate_master_password(master):
        print("Weak or invalid master password. Exiting.")
        return

    db = load_db()
    running = True

    while running:
        print("\nOptions:")
        print("1) Save new password")
        print("2) Retrieve password")
        print("3) Exit")
        print("4) Generate secure password")

        choice = input("> ").strip()

        if choice == "1":
            site = input("Site: ").strip()
            user = input("Username: ").strip()

            print("Do you want to:")
            print("1) Type your own password")
            print("2) Generate a secure password automatically")
            subchoice = input("> ").strip()

            if subchoice == "1":
                pwd = input("Password to store: ").strip()
            elif subchoice == "2":
                pwd = generate_password()
                print(f"Generated password: {pwd}")
            else:
                print("Invalid option.")
                continue

            encrypted_pwd = encrypt(master, pwd)
            db[site] = {"username": user, "password": encrypted_pwd}
            save_db(db)
            print("Password stored securely.")

        elif choice == "2":
            site = input("Site to retrieve: ").strip()

            if site not in db:
                print("No password stored for this site.")
                continue

            stored = db[site]
            try:
                decrypted_pwd = decrypt(master, stored["password"])
                print(f"Password for {site}: {decrypted_pwd}")
            except:
                print("Wrong master password or corrupted data.")
				running = False

        elif choice == "3":
            running = False
            print("Bye!")

        elif choice == "4":
            length = input("Password length (default 16): ").strip()
            if length.isdigit():
                length = int(length)
            else:
                length = 16

            new_pwd = generate_password(length)
            print(f"Generated secure password ({length} chars): {new_pwd}")

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

