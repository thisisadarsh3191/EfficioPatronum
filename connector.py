import mysql.connector as mc

def init():
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root'
        )
        cursor = conn.cursor()
        cursor.execute("create database if not exists UsersEffPat")
        cursor.execute("use UsersEffPat")
        cursor.execute("""
            create table if not exists users (
                name VARCHAR(50) not null,
                user VARCHAR(255) primary key,
                password VARCHAR(255) not null
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                username VARCHAR(255) not null,
                title varchar(255) not null,
                category varchar(255) not null,
                completed boolean default false,
                foreign key (username) references users(user) on delete cascade
            );
        """)
        conn.commit()
    except mc.Error as e:
        print(f"Error: {e}")



def login(username, password):
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root',
            database='UsersEffPat'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from users where user = %s", (username,))
        user = cursor.fetchone()
        
        if user and user['password'] == password:
            return True
        return False
    except mc.Error as e:
        print(f"Login error: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



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
        cursor.execute("select * from users where user = %s", (user,))
        if cursor.fetchone() is not None:
            return False
        cursor.execute("insert into users (name, user, password) VALUES (%s, %s, %s)", (name, user, password))
        conn.commit()
        return True
    except mc.Error as e:
        print(f"Error: {e}")
        return False



def passwordStrength(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    return True



def add_task(username, taskDetails:tuple):
    title = taskDetails[0]
    category = taskDetails[1]
    completed = taskDetails[2] if len(taskDetails) > 2 else False
    
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root',
            database='UsersEffPat'
        )
        cursor = conn.cursor()
        cursor.execute(
            "insert into Tasks (username, title,category,completed) VALUES (%s, %s,%s, %s)",
            (username, title, category, completed)
        )
        conn.commit()
        return True
    except mc.Error as e:
        print(f"Error adding task: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def get_user_tasks(username):
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root',
            database='UsersEffPat'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "select title,category,completed from Tasks where username = %s",(username,)
        )
        return cursor.fetchall()
    except mc.Error as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def deleteTask(task,user):
    try:
        conn = mc.connect(
            host='localhost',
            password='root',
            user="root",
            database='UsersEffPat'
        )
        cursor = conn.cursor()
        title = task['name'] if 'name' in task else task['title']
        cursor.execute("delete from Tasks where username = %s and title = %s", (user, title))
        conn.commit()
        return True
    except mc.Error as e:
        print(f"Error deleting task: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def updateTask(username,title,completed):
    try:
        conn = mc.connect(
            host='localhost',
            user='root',
            password='root',
            database = 'UsersEffPat'
        )
        cursor = conn.cursor()
        cursor.execute("update Tasks set completed=%s where username = %s and title = %s",(completed,username,title))
        conn.commit()
        return True
    except mc.Error as e:
        print(f"Error updating task: {e}")
        return False   
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def changePw(username, new_password):
    try:
        conn = mc.connect(
            host='localhost',
            password='root',
            user="root",
            database='UsersEffPat'
        )
        cursor = conn.cursor()
        cursor.execute(f"update users set password = %s where user = %s", (new_password, username))
        conn.commit()
        return True
    except mc.Error as e:
        print(f"Error changing password: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def deleteAccount(username,password):
    try:
        conn = mc.connect(
            host='localhost',
            username='root',
            password='root',
            database='UsersEffPat'
        )
        cursor = conn.cursor()
        cursor.execute("select password from users where user = %s", (username,))
        result = cursor.fetchone()
        if not password or result[0] != password:
            return False,"Incorrect Password"
        cursor.execute("delete from users where user = %s", (username,))
        conn.commit()
        return True,"User deleted successfully."
    except mc.Error as e:
        print(f"Error deleting account: {e}")
        return False,"Database error occurred."
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()