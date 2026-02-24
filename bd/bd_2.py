import psycopg2
import pandas as pd

def insertValues():
    cursor.execute(
        """
    INSERT INTO locations VALUES ( 2,'Venice','10934');
    INSERT INTO locations VALUES ( 3,'Tokyo', '1689');
    INSERT INTO locations VALUES ( 4,'Hiroshima','6823');
    INSERT INTO locations VALUES ( 5,'Southlake', '26192');
    INSERT INTO locations VALUES ( 6,'South San Francisco', '99236');
    INSERT INTO locations VALUES ( 7,'South Brunswick','50090');
    INSERT INTO locations VALUES ( 9,'Toronto','M5V 2L7');
    INSERT INTO locations VALUES ( 10,'Whitehorse','YSW 9T2');
        """
    )

def add_location_id_column():
    cursor.execute("""
            ALTER TABLE employees 
            ADD COLUMN location_id INTEGER;
            """)

def add_foreign_key():
    cursor.execute("""
    ALTER TABLE employees 
    ADD CONSTRAINT fk_employees_locations 
    FOREIGN KEY (location_id) 
    REFERENCES locations(location_id);
    """)

def update_existing_employees():
    cursor.execute("""
    UPDATE employees 
    SET location_id = CASE 
        WHEN employee_id % 8 = 0 THEN 1
        WHEN employee_id % 8 = 1 THEN 2
        WHEN employee_id % 8 = 2 THEN 3
        WHEN employee_id % 8 = 3 THEN 4
        WHEN employee_id % 8 = 4 THEN 5
        WHEN employee_id % 8 = 5 THEN 6
        WHEN employee_id % 8 = 6 THEN 7
        WHEN employee_id % 8 = 7 THEN 9
        WHEN employee_id % 8 = 0 THEN 10
    END
    WHERE location_id IS NULL;
    """)

def select_employees():
    df = pd.read_sql_query("SELECT * FROM employees ", connection)
    print(df)

def find_john_with_high_salary():
    sql = """
    SELECT *
    FROM employees 
    WHERE first_name = 'John' AND salary > 12000;
    """

    df = pd.read_sql_query(sql, connection)
    print(df)

def find_department_with_max_employees():
    sql = """
    SELECT 
        d.department_name,
        COUNT(e.employee_id) as emp_count
    FROM departments d, employees e
    WHERE d.department_id = e.department_id
    GROUP BY d.department_name
    ORDER BY emp_count DESC
    LIMIT 1;
    """

    df = pd.read_sql_query(sql, connection)
    print(df)

def get_cities_with_high_avg_salary():
    sql = """
    SELECT 
        l.city,
        AVG(e.salary) as avg_salary,
        COUNT(e.employee_id) as emp_count
    FROM locations l
    LEFT JOIN employees e ON l.location_id = e.location_id
    GROUP BY l.city
    HAVING AVG(e.salary) > 8000;
    """

    df = pd.read_sql_query(sql, connection)
    print(df)

def get_employees(city_name):
    cursor.execute("SELECT * FROM count_employees_in_city(%s);", (city_name,))
    for emp in cursor.fetchall():
        print(emp)

def create_count_function():
    cursor.execute("""
    CREATE OR REPLACE FUNCTION count_employees_in_city(city_name VARCHAR)
    RETURNS INTEGER AS $$
    DECLARE
        emp_count INTEGER;
    BEGIN
        SELECT COUNT(e.employee_id) INTO emp_count
        FROM employees e
        JOIN locations l ON e.location_id = l.location_id
        WHERE l.city = city_name;

        RETURN emp_count;
    END;
    $$ LANGUAGE plpgsql;
    """)

if __name__ == "__main__":
    connection = psycopg2.connect(database="students", user="postgres", password="bd2", host="127.0.0.1", port="5432")
    cursor = connection.cursor()

    get_employees("Roma")

    connection.commit()
    cursor.close()
    connection.close()