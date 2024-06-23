# sql.py
# SQL Backend Implementation

import psycopg2
from app.util import *
import datetime
import random

# host		IP地址
# user      用户名
# password  密码
# database  数据库名称

class SQL_Server():
	def __init__(self, host='db', user='postgres', password='123456', database='hospital', autocommit=True):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.autocommit = autocommit
		# following varibles are for data base
		self.tableList = None
		self.attributeList = None

	def connection(self):
		conn = psycopg2.connect(
			host=self.host, 
			user=self.user, 
			password=self.password, 
			dbname=self.database
		)
		return conn

	def loginDetect(self, username, password):
		conn = self.connection()
		cursor = conn.cursor()
		username = "'" + username + "'"
		password = "'" + password + "'"
		cursor.execute('SELECT * FROM administer WHERE admin = ' + username + ' and password = ' + password + ';')
		results = cursor.fetchall()
		cursor.close()
		conn.close()
		return results

	def register(self, username, password):
		# try to insert (username, password) into USERTABLE
		conn = self.connection()
		cursor = conn.cursor()
		username = "'" + username + "'"
		password = "'" + password + "'"
		statement = '(' + username + ', ' + password + ')'
		return self.insertIntoTable('administer', statement)

	def getTAList(self):
		# get table list
		self.getTableList()

		# get attribute list for each table
		self.getAttributeList()

	def tableDetect(self, tablename):
		# update table and attribute
		self.getTAList()

		if tablename in self.tableList:
			return True
		return False

	def getAttributeListOfTable(self, table):
		index = getIndex(table, self.tableList)
		return self.attributeList[index]

	def getAttributeListForSelectShow(self, table, attribute):
		if attribute == '*':
			return self.getAttributeListOfTable(table)
		return [attribute]

		def selectFromTable(self, table, selected_option, attribute):
		# update table and attribute
		self.getTAList()

		# SQL query
		conn = self.connection()
		cursor = conn.cursor()
		try:
			if table == 'MAKE' or table == 'ASSEMBLE':
				if selected_option != ' ' and attribute != ' ':
					str = 'SELECT ' + '*' + ' FROM ' + table + ' Where ' + selected_option + '=' + '\'' + attribute + '\''
				elif selected_option == ' ' and attribute != ' ':
					str = 'SELECT ' + selected_option + ' FROM ' + table
				else:
					str = 'SELECT ' + '*' + ' FROM ' + table
				cursor.execute(str)
			else:
				if selected_option != ' ' and attribute != ' ':
					str = 'SELECT ' + '*' + ' FROM ' + table + ' Where ' + selected_option + '=' + '\'' + attribute + '\''
				elif selected_option == ' ' and attribute != ' ':
					str = 'SELECT ' + selected_option + ' FROM ' + table
				else:
					str = 'SELECT ' + '*' + ' FROM ' + table
				print("str=",str)
				cursor.execute(str)
			results = cursor.fetchall()
			return results
		except Exception as e:
			print ('No such query, input again')
		else:
			index = getIndex(table, self.tableList)
			showResults(table, self.attributeList[index], attribute, results)
		finally:
			cursor.close()
			conn.close()

	def insertIntoTable(self, table, insertSQL):
		# update table and attribute
		self.getTAList()

		statement = insertSQL

		# SQL query
		conn = self.connection()
		cursor = conn.cursor()
		try:
			cursor.execute('INSERT INTO ' + table + ' VALUES ' + statement)
			conn.commit()  # 提交事务
		except Exception as e:
			print ('Something error')
			return 'Failed'
		else:
			print ('Succeed')
			return 'Succeeded'
		finally:
			cursor.close()
			conn.close()

	def deleteFromUserTable(self, table, deleteSQL):
		# update table and attribute
		self.getTAList()

		statement = deleteSQL

		# SQL query
		conn = self.connection()
		cursor = conn.cursor()
		try:
			cursor.execute('DELETE FROM ' + table + ' WHERE ' + statement)
			conn.commit()  # 提交事务
		except Exception as e:
			print ('Something error, please input again')
			return 'Failed'
		else:
			print ('Succeed or no such value')
			return 'Succeeded'
		finally:
			cursor.close()
			conn.close()

	def dropTable(self, table):
		# update table and attribute
		self.getTAList()

		# SQL query
		conn = self.connection()
		cursor = conn.cursor()
		try:
			cursor.execute('DROP TABLE ' + table)
			conn.commit()  # 提交事务
		except Exception as e:
			print ('Something error, please input again')
			return 'Failed'
		else:
			print ('Succeed')
			return 'Succeeded'
		finally:
			cursor.close()
			conn.close()

	def generate_id(self, table, attribute):
		while True:
			id = str(random.randint(1000, 9999))  # Generate a random number between 1000 and 9999
			results = self.selectFromTable(table, attribute, ' ')
			if id not in [result[0] for result in results]:
				break
		return id

	def getTableList(self):
		# get table list
		conn = self.connection()
		cursor = conn.cursor()
		#cursor.execute("SELECT Name FROM SysObjects WHERE XType='U' ORDER BY Name")
		cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")
		self.tableList = cursor.fetchall()
		for i in range(len(self.tableList)):
			self.tableList[i] = self.tableList[i][0]
		cursor.close()
		conn.close()

	def getAttributeList(self):
		# get attribute list for each table
		conn = self.connection()
		cursor = conn.cursor()
		self.attributeList = []
		for table in self.tableList:
			cursor.execute("SELECT column_name FROM information_schema.COLUMNS WHERE table_name='" + table + "'")
			temp = cursor.fetchall()
			for i in range(len(temp)):
				temp[i] = temp[i][0]
			self.attributeList.append(temp)
		cursor.close()
		conn.close()
