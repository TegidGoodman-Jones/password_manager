import sqlite3
from sqlite3 import Error
import cryption


def create_connection(database):

	conn = None

	try:
		conn = sqlite3.connect(database) # creating connection to database
		return conn
	
	except Error as e:
		print(e)

	return conn


def create_table(conn, sql):

	try:
		c = conn.cursor()
		c.execute(sql)  # executing the sql code from the main()
	
	except Error as e:
		print(e)


def add_password(conn):

	sql = '''INSERT INTO passwords(name,password,date_added)VALUES(?,?,?)'''

	name = str(input('What is the password for?:  '))
	password = str(input('What is the password?:  '))
	date = str(input('Date today (00/00/00)?:  '))

	encrypted_password = cryption.encrypt_password(password)  # encrypting password

	entry = (name, encrypted_password, date)  # putting all values in a list (order of values in !important)

	c = conn.cursor()
	c.execute(sql, entry)
	conn.commit()  # vital, will not work without this


def update_password(conn):

	sql = '''UPDATE passwords
		SET password = ?,
		date_added = ?
		WHERE name = ?'''

	name = str(input('Which password would you like to change?:  '))  # must be existing name
	password = str(input('What is the password?:  '))
	date = str(input('Date today (00/00/00)?:  '))

	encrypted_password = cryption.encrypt_password(password)  # encryptng password

	entry = (encrypted_password, date, name)  # putting all values in a list (order of values in !important)

	c = conn.cursor()
	c.execute(sql, entry)
	conn.commit()  # commiting changes, very important


def delete_password(conn):

	sql = 'DELETE FROM passwords WHERE name = ?'

	name = str(input('Which password would you like to delete?:  '))  # exsisting name only

	c = conn.cursor()
	c.execute(sql, (name,))
	conn.commit()  # COMMIT


def get_password(conn):

	sql = 'SELECT * FROM passwords WHERE name = ?'  # gathering results that fit params

	name = str(input('Which password would you like to get?:  '))  # existing name only

	c = conn.cursor()
	c.execute(sql, (name,))

	results = c.fetchall()

	for result in results:
		print('\nname = {}'.format(result[0]))
		
		password = cryption.decrypt_password(result[1])  # decrypting the password to readable format
		print('password = {}'.format(password))

def get_all_passwords(conn):

	sql = 'SELECT * FROM passwords'


	c = conn.cursor()
	c.execute(sql)

	results = c.fetchall()

	for result in results:
		print('\nname = {}'.format(result[0]))
		password = cryption.decrypt_password(result[1])
		print('password = {}\n'.format(password))


def ui(conn):

	print('PASSWORD MANAGER!\n\n')

	exit = False
	
	while exit == False:
		# gathering what user wants
		response = input('\nAdd password?(a)\nUpdate password?(b)\nDelete password?(c)\nGet password?(d)\nGet all passwords?(e)\nQuit (q)\n\n:  ')

		if response == 'a':
			add_password(conn)
			print('Password added')
	
		elif response == 'b':
			update_password(conn)
			print('Password updated!')
	
		elif response == 'c':
			delete_password(conn)
			print('Password deleted!')

		elif response == 'd':
			get_password(conn)

		elif response == 'e':
			get_all_passwords(conn)

		elif response == 'q':
			exit = True
			print('\nGoodbye! ')


def main():

	database = 'pass_manager.db'  # database file

	sql = """ CREATE TABLE IF NOT EXISTS passwords(   # params for the database table, changeable
		name TEXT PRIMARY KEY,
		password BLOB NOT NULL,
		date_added TEXT
		); """

	conn = create_connection(database)

	
	if conn is None:
		create_table(conn, sql)

	ui(conn)  # running the user interface


	conn.close()  # closing connection



if __name__ == '__main__':
	
	main()


