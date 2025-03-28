import MySQLdb
import hashlib
import random

def get_salt():
    random_source = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    salt = ""
    for i in range(20):
        salt += random.choice(random_source)
    return salt

def get_hashed_password(plain_pw, salt):
    hashed_pw = hashlib.pbkdf2_hmac("sha256", plain_pw.encode(), salt.encode(), 19720).hex()
    return hashed_pw

def get_connection():
    connection = MySQLdb.connect(user='root',
                                password='morijyobi',
                                host='localhost',
                                database='spring_vacation',)
    return connection

def insert_user(username, plain_pw):
    salt = get_salt()
    hashed_pw = get_hashed_password(plain_pw, salt)

    connection = get_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO users (username, salt, password_hash) VALUES (%s, %s, %s)"
    cursor.execute(sql, (username, salt, hashed_pw))

    connection.commit()
    cursor.close()
    connection.close()

def get_account_by_name(username):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT user_id, username, salt, password_hash FROM users WHERE username = %s"

    cursor.execute(sql, (username,))
    account = cursor.fetchone()
    cursor.close()
    connection.close()

    return account

def login(pw, username):
    account = get_account_by_name(username)
    if account is None:
        return None

    hashed_db_pw = account[3]
    salt = account[2]
    hashed_input_pw = get_hashed_password(pw, salt)

    if hashed_db_pw == hashed_input_pw:
        return account
    else:
        return None

def insert_treeview():
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT * FROM books'
    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def add_to_cart(user_id, book_id, quantity=1):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO cart (user_id, book_id, quantity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, book_id, quantity))

    connection.commit()
    cursor.close()
    connection.close()

def register_borrowed_book(user_id, book_id):
    connection = get_connection()
    cursor = connection.cursor()

    # データを借りた状態として挿入
    cursor.execute("""
        INSERT INTO borrowed_books (user_id, book_id, borrow_date, returned)
        VALUES (%s, %s, CURRENT_DATE, FALSE)
    """, (user_id, book_id))

    connection.commit()
    cursor.close()
    connection.close()

def delete_cart_item(user_id, book_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "DELETE FROM cart WHERE user_id = %s AND book_id = %s"
    cursor.execute(sql, (user_id, book_id))

    connection.commit()
    cursor.close()
    connection.close()
    
def search_products(query):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        SELECT * FROM books
        WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s
    """
    search_query = f"%{query}%"
    cursor.execute(sql, (search_query, search_query, search_query))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows