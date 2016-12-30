import sqlite3
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
DATABASE = cur_dir+'/tanyas_job.db'



def connect_db():
	conn = sqlite3.connect(DATABASE)
	return conn

def close_db():
	conn = connect_db()
	conn.close()

def create_email(email):
	conn = connect_db()
	c = conn.cursor()
	c.execute("INSERT INTO emails (email, emailed) VALUES (?, ?)", (email, 0))
	conn.commit()
	close_db()	

def get_emails():
	conn = connect_db()
	c = conn.cursor()
	e = c.execute('SELECT email FROM emails WHERE emailed = 0')
	emails = e.fetchall()
	close_db()
	return emails

def checkifexists(email):
	conn = connect_db()
	c = conn.cursor()
	e = c.execute("SELECT id FROM emails WHERE email = ?", (email,))
	data = e.fetchall()
	close_db()
	if len(data)==0:
	 	return False
	else:
		return True

def checkifvisited(link):
	conn = connect_db()
	c = conn.cursor()
	e = c.execute("SELECT id FROM visited WHERE link = ?", (link,))
	data = e.fetchall()
	close_db()
	if len(data)==0:
	 	return False
	else:
		return True


def save_visited(link):
	conn = connect_db()
	c = conn.cursor()
	c.execute("INSERT INTO visited (link) VALUES (?)", (link,))
	conn.commit()
	close_db()

def setEmailed(email):
	conn = connect_db()
	c = conn.cursor()
	c.execute('UPDATE emails SET emailed=1 WHERE email=?', (email,))
	conn.commit()