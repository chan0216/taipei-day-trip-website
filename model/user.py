from common.config.db_config import con_pool
from common.utils.error_util import EmailException
import re


def user_signup(data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        name = data["name"]
        email = data["email"]
        password = data["password"]
        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        userEmail = cursor.fetchone()      
        if userEmail is None:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                            (name, email, password))
            db.commit()
            return True
        else:
            raise EmailException("註冊失敗, Email已註冊過")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()


def user_signin(data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        email = data["email"]
        password = data["password"]
        cursor.execute(
            "SELECT id,email,password FROM users WHERE email=%s and password=%s", (email, password))
        user_data = cursor.fetchone()
        return user_data
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def get_user(data):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "SELECT id,name,email FROM users WHERE email=%s", (data["user"],))
        user_data = cursor.fetchone()
        return user_data
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
