import json
from pathlib import Path

db_file = Path("users.json")

def load_users():
    if db_file.exists():
        return json.loads(db_file.read_text())
    return {}

def save_users(data):
    db_file.write_text(json.dumps(data, indent=4))

def is_registered(user_id):
    users = load_users()
    return str(user_id) in users

def register_user(user_id, name, phone):
    users = load_users()
    users[str(user_id)] = {"name": name, "phone": phone}
    save_users(users)
