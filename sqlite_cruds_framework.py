# CRUDS framework program using sqlite3

import sqlite3
connection = sqlite3.connect("C:\\Users\\tharu\\framework.db")
cursor = connection.cursor()
config_table_name = "fw_config"
table_name = cursor.execute("select value from " + config_table_name +" where key = ?", ("title",)).fetchall()
table_name = table_name[0][0]
headers = cursor.execute("PRAGMA table_info(" + table_name + ")").fetchall()
column_names = [data[1] for data in headers]

def add_new_record():
    values=[]
    for field in column_names:
        values.append(input("enter the " + field + " : "))
    values = tuple(values)
    cursor.execute("insert into " + table_name + " values" + str(values))

def show_records():
    print(" | ".join(str(value) for value in column_names))
    rows = cursor.execute("select * from " + table_name).fetchall()
    for row in rows:
        print(" | ".join(str(value) for value in row))

def select_option(task):
    for index, field in enumerate(column_names):
        print(str(index) + ". " + field)
    return int(input("Enter your choice to " + task + ": ")) 

def update_record():
    record_id = input("Enter " + column_names[0] + " to update : ")
    choice = select_option("update")
    cursor.execute("update " + table_name +" set " + column_names[choice] + " = ? where " + column_names[0] +" = ?", (input("enter the new update value: "), record_id))

def delete_record():
    record_id = input("Enter " + column_names[0] + " to delete : ")
    cursor.execute("delete from " + table_name + " where " + column_names[0] + " = ?", (record_id,))
    print(cursor.execute("select value from "+ config_table_name +" where key = ?", ("saved_msg",)).fetchall()[0][0])

def menu():
    menu_values = cursor.execute("select value from "+ config_table_name +" where key = ?", ("menu",)).fetchall()
    print(menu_values[0][0].replace("\\n", "\n"))
    choice = int(input("Enter your choice: "))
    menu_options[choice-1]()
    connection.commit()
    menu()

menu_options = [add_new_record, show_records, update_record, delete_record, exit]
menu()
