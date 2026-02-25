import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_connection():
    connection = psycopg2.connect(
        database="students",
        user="postgres",
        password="bd2",
        host="127.0.0.1",
        port="5432"
    )
    return connection


def plot_locations_graph(connection):
    """Построение графика по городам и количеству локаций"""
    query = """
    SELECT city, COUNT(*) as location_count
    FROM locations
    GROUP BY city
    ORDER BY location_count DESC
    """
    df = pd.read_sql_query(query, connection)

    plt.figure(figsize=(12, 6))
    plt.bar(df['city'], df['location_count'], color='green', alpha=0.7)
    plt.title('Количество локаций по городам', fontsize=16)
    plt.xlabel('Город', fontsize=12)
    plt.ylabel('Количество локаций', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return df


def plot_employees_by_name(connection):
    """По оси х – имя сотрудника, по оси у – количество сотрудников с таким именем"""
    query = """
    SELECT first_name, COUNT(*) as name_count
    FROM employees
    GROUP BY first_name
    ORDER BY name_count DESC, first_name
    """
    df = pd.read_sql_query(query, connection)

    plt.figure(figsize=(14, 6))
    plt.bar(df['first_name'], df['name_count'], color='skyblue', edgecolor='navy')
    plt.title('Распределение сотрудников по именам', fontsize=16)
    plt.xlabel('Имя сотрудника', fontsize=12)
    plt.ylabel('Количество сотрудников', fontsize=12)
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.show()

    return df

def plot_salary_by_job(connection):
    """По оси х – должность сотрудника, по оси у – суммарная заработная плата"""
    query = """
    SELECT j.job_title, SUM(e.salary) as total_salary
    FROM employees e
    JOIN jobs j ON e.job_id = j.job_id
    GROUP BY j.job_title
    ORDER BY total_salary DESC
    """
    df = pd.read_sql_query(query, connection)

    plt.figure(figsize=(14, 6))
    plt.bar(df['job_title'], df['total_salary'], color='lightcoral', edgecolor='darkred')
    plt.title('Суммарная зарплата по должностям', fontsize=16)
    plt.xlabel('Должность', fontsize=12)
    plt.ylabel('Суммарная зарплата', fontsize=12)
    plt.xticks(rotation=45, ha='right')


    plt.tight_layout()
    plt.show()

    return df


def plot_modified_graph1(connection, names_list=None):
    """
    Модифицированный график 1: горизонтальный, с измененными цветами
    и условием по списку имен
    """
    if names_list is None:
        names_list = ['Steven', 'John', 'David', 'Michael']

    names_tuple = tuple(names_list)

    query = f"""
    SELECT first_name, COUNT(*) as name_count
    FROM employees
    WHERE first_name IN {names_tuple}
    GROUP BY first_name
    ORDER BY name_count DESC
    """
    df = pd.read_sql_query(query, connection)

    plt.figure(figsize=(10, 6))

    plt.barh(df['first_name'], df['name_count'],
                    color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    plt.title(f'Количество сотрудников с именами {", ".join(names_list)}', fontsize=16)
    plt.xlabel('Количество сотрудников', fontsize=12)
    plt.ylabel('Имя сотрудника', fontsize=12)


    plt.tight_layout()
    plt.show()

    return df


def plot_salary_by_job_with_range(connection, min_salary, max_salary):
    """
    Функция для построения графика по должностям с фильтром по диапазону суммарной зарплаты
    """
    query = """
    SELECT j.job_title, SUM(e.salary) as total_salary
    FROM employees e
    JOIN jobs j ON e.job_id = j.job_id
    GROUP BY j.job_title
    HAVING SUM(e.salary) BETWEEN %s AND %s
    ORDER BY total_salary DESC
    """
    df = pd.read_sql_query(query, connection, params=(min_salary, max_salary))

    if df.empty:
        print(f"Нет данных для диапазона зарплат от {min_salary} до {max_salary}")
        return df

    plt.figure(figsize=(12, 6))

    colors = plt.cm.viridis(np.linspace(0, 1, len(df)))
    plt.barh(df['job_title'], df['total_salary'], color=colors)

    plt.title(f'Суммарная зарплата по должностям\n(диапазон: {min_salary:,} - {max_salary:,})',
              fontsize=16)
    plt.xlabel('Суммарная зарплата', fontsize=12)
    plt.ylabel('Должность', fontsize=12)

    plt.tight_layout()
    plt.show()

    return df


if __name__ == "__main__":
    connection = create_connection()

    plot_employees_by_name(connection)

    plot_salary_by_job(connection)

    selected_names = ['Steven', 'John', 'David', 'Michael', 'Peter']
    plot_modified_graph1(connection, selected_names)

    plot_salary_by_job_with_range(connection, 20000, 50000)

    plot_locations_graph(connection)

    connection.close()