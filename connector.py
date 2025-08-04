import mysql.connector as mc

def init():
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root'
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS UsersEffPat")
        cursor.execute("USE UsersEffPat")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                name VARCHAR(50) NOT NULL,
                user VARCHAR(255) primary key,
                password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
    except mc.Error as e:
        print(f"Error: {e}")

def login(user, password):
    
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root',
            database='UsersEffPat'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user = %s", (user,))
        user_row = cursor.fetchone()
        if user_row and user_row["password"] == password:
            return True
        else:
            return False
    except mc.Error as e:
        print(f"Error: {e}")
        return False

strength = {
    1: "Password must be at least 8 characters long.",
    2: "Password must contain at least one digit.",
    3: "Password must contain at least one uppercase letter.",
    4: "Password must contain at least one lowercase letter."
}

def register(name, user, password):
    try:
        check = passwordStrength(password)
        if check is not True:
            return strength[check]
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root',
            database='UsersEffPat'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user = %s", (user,))
        if cursor.fetchone() is not None:
            return False
        cursor.execute("INSERT INTO users (name, user, password) VALUES (%s, %s, %s)", (name, user, password))
        conn.commit()
        return True
    except mc.Error as e:
        print(f"Error: {e}")
        return False

def passwordStrength(password):
    if len(password) < 8:
        return 1
    if not any(char.isdigit() for char in password):
        return 2
    if not any(char.isupper() for char in password):
        return 3
    if not any(char.islower() for char in password):
        return 4
    return True
