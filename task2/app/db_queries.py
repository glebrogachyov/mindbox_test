import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def db_connection():
    conn = psycopg2.connect(
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn


def db_get_products():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from information_schema.tables where table_name=%s", ('product',))
    is_table_exist = bool(cur.rowcount)
    if not is_table_exist:
        return "error. table doesn't exist."
    query = '''
            SELECT product_name, category_name
            FROM product
            LEFT JOIN product_to_category USING(product_id)
            LEFT JOIN category USING(category_id)
    '''
    cur.execute(query)
    res = cur.fetchall()
    conn.close()
    return res


def db_get_categories():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from information_schema.tables where table_name=%s", ('category',))
    is_table_exist = bool(cur.rowcount)
    if not is_table_exist:
        return "error. table doesn't exist."
    query = '''
            SELECT category_name, product_name
            FROM category
            LEFT JOIN product_to_category USING(category_id)
            LEFT JOIN product USING(product_id)
    '''
    cur.execute(query)
    res = cur.fetchall()
    conn.close()
    return res


def db_get_product_to_category():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from information_schema.tables where table_name=%s", ('product_to_category',))
    is_table_exist = bool(cur.rowcount)
    if not is_table_exist:
        return "error. table doesn't exist."
    query = '''
            SELECT product_name, category_name
            FROM product_to_category
            JOIN product USING(product_id)
            JOIN category USING(category_id)
    '''
    cur.execute(query)
    res = cur.fetchall()
    conn.close()
    return res


def db_init_table():
    # print("entry to init table")
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("select * from information_schema.tables where table_name=%s", ('category',))
    is_category_exist = bool(cur.rowcount)
    cur.execute('''CREATE TABLE IF NOT EXISTS category(category_id serial PRIMARY KEY, 
                                                       category_name VARCHAR(30) UNIQUE NOT NULL);''')
    if not is_category_exist:
        cur.execute('''
                   INSERT INTO category(category_name)
                   values ('Молочные продукты'), ('Мясо'), ('Здоровая еда'), ('Сладкое'), ('Выпечка'),
                   ('Фрукты, овощи'), ('Напитки'), ('Спортивное питание');''')
        # print('data added to "category"')

    cur.execute("select * from information_schema.tables where table_name=%s", ('product',))
    is_product_exist = bool(cur.rowcount)
    cur.execute('''CREATE TABLE IF NOT EXISTS product(product_id serial PRIMARY KEY, 
                                                      product_name VARCHAR(30) UNIQUE NOT NULL);''')
    if not is_product_exist:
        cur.execute('''
                   INSERT INTO product(product_name)
                   values ('Молоко'), ('Сыр'), ('Брюссельская капуста'), ('Торт "Муравейник"'),
                   ('Говядина'), ('Хурма'), ('Лимонад'), ('Чипсы');''')
        # print('data added to "product"')

    cur.execute("select * from information_schema.tables where table_name=%s", ('product_to_category',))
    is_prod_to_cat_exist = bool(cur.rowcount)
    cur.execute('''CREATE TABLE IF NOT EXISTS product_to_category(id serial PRIMARY KEY,
                                                                  product_id INT NOT NULL,
                                                                  category_id INT NOT NULL,
                                                                  CONSTRAINT fk_category_id FOREIGN KEY (category_id)
                                                                  REFERENCES category (category_id) ON DELETE CASCADE,
                                                                  CONSTRAINT fk_product_id FOREIGN KEY (product_id)
                                                                  REFERENCES product (product_id) ON DELETE CASCADE);
                   CREATE UNIQUE INDEX IF NOT EXISTS ui_product_to_category_prod_id_cat_id
                                                     ON product_to_category(product_id, category_id);''')
    if not is_prod_to_cat_exist:
        cur.execute('''
                   INSERT INTO product_to_category(product_id, category_id)
                   values (1, 1), (1, 7), (1, 3), (2, 1), (2, 3), (3, 3), (3, 6),
                   (4, 4), (4, 5), (5, 2), (5, 3), (6, 6), (7, 4), (7, 7)''')
        # print('data added to "product_to_category"')
    conn.commit()
    conn.close()
    cur.close()
    return 'done.'
