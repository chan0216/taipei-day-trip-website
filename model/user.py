from model.public import con_pool
import re


def user_signup(data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        name = data["name"]
        email = data["email"]
        password = data["password"]
        cursor.execute("SELECT email FROM user WHERE email=%s", (email,))
        userEmail = cursor.fetchone()
        pattern = re.compile("^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$")
        if userEmail is None:
            if pattern.match(email):
                cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
                               (name, email, password))
                return "ok"
        else:
            return "重複的Email"
    except:
        db.rollback()
        return "error"
    finally:
        cursor.close()
        db.commit()
        db.close()


def user_signin(data):
    try:

        email = data["email"]
        password = data["password"]
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "SELECT id,email,password FROM user WHERE email=%s and password=%s", (email, password))
        userData = cursor.fetchone()
        return userData
    except:
        return "error"
    finally:
        cursor.close()
        db.close()


def user_data(data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "SELECT id,name,email FROM user WHERE email=%s", (data["user"],))
        userData = cursor.fetchone()
        return userData
    finally:
        cursor.close()
        db.close()
