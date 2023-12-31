import psycopg2
from services.passwordHash import hashFunc
from dotenv import load_dotenv
import os

load_dotenv()

def adminPassHash():
      password = os.getenv('ADMIN_PASSWORD')
      hashed = hashFunc(password)
      return hashed

def connect():
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_STRING'))
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f'an error occured: {e}')

def initialize():
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_STRING'))
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, password TEXT NOT NULL, username TEXT NOT NULL, email TEXT UNIQUE NOT NULL, balance FLOAT NOT NULL DEFAULT 0, role TEXT DEFAULT %s);', ('user',))
        conn.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS image (id SERIAL PRIMARY KEY, user_id INT NOT NULL, image_url VARCHAR(255) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);')
        conn.commit()
        cur.execute('INSERT INTO users (username, email, password, balance, role) SELECT %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM users WHERE role = %s);', (os.getenv('ADMIN_USERNAME'), os.getenv('ADMIN_EMAIL'), adminPassHash(), 0.0, 'admin', 'admin'))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f'an error occured: {e}')