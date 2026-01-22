"""Small helper to create or update an admin user in data/users.db

Usage:
  python scripts/setup_admin.py --email admin@example.com --name "Admin Name"
  (you will be prompted for a password if not provided)

The script inserts/updates the user row and sets a hashed password compatible with the app.
To make the email an active admin, set the ADMIN_EMAILS environment variable, e.g.:
  setx ADMIN_EMAILS "admin@example.com"
or on PowerShell for current session:
  $env:ADMIN_EMAILS = 'admin@example.com'

Note: This script does not edit `app.py`. Instead prefer setting `ADMIN_EMAILS` using environment variables.
"""

import argparse
import getpass
import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join('data', 'users.db')

CREATE_USERS_SQL = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mobile TEXT,
    password_hash TEXT NOT NULL,
    security_question TEXT,
    answer TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,
    marks TEXT,
    notes TEXT,
    chat_permission INTEGER DEFAULT 1
)
'''


def upsert_admin(name, email, password):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(CREATE_USERS_SQL)
    cur.execute('SELECT id FROM users WHERE email = ?', (email,))
    row = cur.fetchone()
    password_hash = generate_password_hash(password)
    if row:
        cur.execute('UPDATE users SET name = ?, password_hash = ? WHERE email = ?', (name, password_hash, email))
        print(f"Updated admin user: {email}")
    else:
        cur.execute('INSERT INTO users (name, email, mobile, password_hash, security_question, answer) VALUES (?, ?, ?, ?, ?, ?)',
                    (name, email, '', password_hash, '', ''))
        print(f"Created admin user: {email}")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create or update an admin user in data/users.db')
    parser.add_argument('--email', '-e', required=True, help='Admin email')
    parser.add_argument('--name', '-n', default='Admin', help='Admin full name')
    parser.add_argument('--password', '-p', help='Password (if omitted, will prompt)')
    args = parser.parse_args()

    pwd = args.password
    if not pwd:
        pwd = getpass.getpass('Enter new password: ')
        pwd2 = getpass.getpass('Confirm password: ')
        if pwd != pwd2:
            print('Passwords do not match. Exiting.')
            raise SystemExit(1)

    upsert_admin(args.name, args.email, pwd)
    print('\nNext step: ensure the admin email is present in ADMIN_EMAILS for the running app. You can set it via environment variable:')
    print("  PowerShell (per-session): $env:ADMIN_EMAILS = 'admin@example.com'")
    print("  Windows (permanent): setx ADMIN_EMAILS \"admin@example.com\"")
    print('Restart the server after making changes.')
