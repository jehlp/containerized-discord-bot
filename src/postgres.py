import os
from time import sleep

# Not part of stdlib
import psycopg2

def connect_db(retries=5, delay=5):
    while retries > 0:
        try:
            return psycopg2.connect(os.getenv('DATABASE_URL'))
        except psycopg2.OperationalError as e:
            print(f"Database connection failed, retrying in {delay} seconds...")
            sleep(delay)
            retries -= 1
    raise Exception("Failed to connect to the database after several attempts.")

def get_user_xp(user_id):
    sql = """
    SELECT xp 
    FROM users
    WHERE user_id = %s
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            xp = cur.fetchone()
            return xp[0] if xp else None

def update_user_xp(user_id, xp_increment):
    sql = """
    INSERT INTO users (user_id, xp) 
    VALUES (%s, %s) 
    ON CONFLICT (user_id) 
    DO UPDATE SET xp = users.xp + excluded.xp
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id, xp_increment))
            conn.commit()

