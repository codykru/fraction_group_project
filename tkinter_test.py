from tkinter import *
import MySQLdb
import random
import operator
import fractions

#USERS TABLE SCHEMA
#+----------+-------------+------+-----+---------+----------------+
#| Field    | Type        | Null | Key | Default | Extra          |
#+----------+-------------+------+-----+---------+----------------+
#| id       | int(11)     | NO   | PRI | NULL    | auto_increment |
#| username | varchar(30) | YES  |     | NULL    |                |
#| password | varchar(15) | YES  |     | NULL    |                |
#| score    | double      | YES  |     | NULL    |                |
#+----------+-------------+------+-----+---------+----------------+

#FIXMES AND BUGS INCLUDED, SATISFACTION NOT GUARANTEED!

class MyApp:

	#input: parent object, should be root
	#output: 
	#description: initial login screen, calls login functions for application
	def __init__(self, myParent):
		print("app initialized...")
		self.username_master = ""
		self.parent = myParent

		#create and pack container
		self.myContainer1 = Frame(myParent)
		self.myContainer1.pack()

		self.prompt = Label(self.myContainer1, text="Please Enter your Account Credentials:")
		self.prompt.pack(side="top", fill='both', expand=True, padx=6, pady=20)

		#create and pack input fields from username, password
		Label(self.myContainer1, text="Username").pack(side="top", fill='both', expand=True, padx=4, pady=4)
		self.username = Entry(self.myContainer1)
		self.username.pack(side="top", fill='both', expand=True, padx=4, pady=4)
		Label(self.myContainer1, text="Password").pack(side="top", fill='both', expand=True, padx=4, pady=4)
		self.password = Entry(self.myContainer1, show="*", width=15)
		self.password.pack(side="top", fill='both', expand=True, padx=4, pady=4)

		#creation of login button, binding to appropriate actions
		self.button1 = Button(self.myContainer1)
		self.button1["text"] = "Login"
		self.button1.pack(side="top", fill='both', expand=True, padx=4, pady=4)
		self.button1.bind("<Button-1>", self.loginClick)

		#creation of user creation button, binding to appropriate actions
		self.button2 = Button(self.myContainer1)
		self.button2["text"] = "Create Account"
		self.button2.pack(side="top", fill='both', expand=True, padx=4, pady=4)
		self.button2.bind("<Button-1>", self.createClick)

	#input:
	#output: 
	#description: displays navigation bar, used only for function calls, no other interaction
	def navBar(self):
		self.myContainer1 = Frame(self.parent, width=600, height=100, bd = 1, relief = GROOVE)
		self.myContainer1.pack(padx = 5, pady = 5)

		#creation of solver, quizzer, view results, and quit buttons, binding to appropriate actions
		self.solver_button = Button(self.myContainer1, height = 2, width = 10)
		self.solver_button["text"] = "Solver"
		self.solver_button.grid(row = 0, column = 0, padx = 10, pady = 10)
		self.solver_button.bind("<Button-1>", self.startSolver)

		self.quizzer_button = Button(self.myContainer1, height = 2, width = 10)
		self.quizzer_button["text"] = "Quizzer"
		self.quizzer_button.grid(row = 0, column = 1, padx = 10, pady = 10)
		self.quizzer_button.bind("<Button-1>", self.startQuizzer)

		self.results_button = Button(self.myContainer1, height = 2, width = 10)
		self.results_button["text"] = "View Results"
		self.results_button.grid(row = 0, column = 2, padx = 10, pady = 10)
		self.results_button.bind("<Button-1>", self.startResults)

		self.quit_button = Button(self.myContainer1, height = 2, width = 10, bg="lightgrey")
		self.quit_button["text"] = "Quit"
		self.quit_button.grid(row = 0, column = 3, padx = 10, pady = 10)
		self.quit_button.bind("<Button-1>", self.quit)

		self.account_info = Label(self.myContainer1, text=self.username_master)
		self.account_info.grid(row = 0, column = 4, padx = 10, pady = 10)

		self.score_info = Label(self.myContainer1, text="score: " + str(self.get_users_score(self.username_master)))
		self.score_info.grid(row = 0, column = 5, padx = 10, pady = 10)


	#input:
	#output: 
	#description: display main menu
	def mainMenu(self):
		print("main menu initialized...")

		#destroy and resize orginal frame
		self.myContainer1.destroy()
		self.parent.minsize(width=700, height=500)

		#create the navigation bar
		self.navBar()

		#create second container
		self.myContainer2 = Frame(self.parent, width=600, height=500, bd = 1, relief = GROOVE)
		self.myContainer2.pack(padx = 5, pady = 5)

		#main menu title label
		self.name = Label(self.myContainer2, text="Main Menu", height = 3, width = 13, font=(25))
		self.name.pack(anchor=CENTER)

		#create large text box to display main menu info, along with scroll bar
		self.scroll_bar = Scrollbar(self.myContainer2)
		self.text_object = Text(self.myContainer2, height=20, width=80)
		self.scroll_bar.pack(side=RIGHT, fill=Y)
		self.text_object.pack(side=LEFT, fill=Y)
		self.scroll_bar.config(command=self.text_object.yview)
		self.text_object.config(yscrollcommand=self.scroll_bar.set)
		self.quote = """Welcome to Fractions Helper, the Fraction solver and quizzer.
						Please use the navigation bar at the top to access the various 
						modules within the application. Below is a brief summary of the
						application:

						-login / authentication
						-main menu
						-fraction solver
						-fraction quizzing
						-review of your scores

						Version 0.2"""
		
		self.text_object.insert(END, self.quote)
		self.text_object.config(state=DISABLED)

	#input: event object
	#output: 
	#description: two fractions, an operator, a solve button
	def startQuizzer(self, event):
		print("quizzer initialized...")

		#destroy and resize orginal frame
		self.myContainer1.destroy()
		self.myContainer2.destroy()
		self.parent.minsize(width=700, height=500)

		try:
			self.base1.destroy()
		except:
			print("base1 does not exist")

		#create the navigation bar
		self.navBar()

		#create base frame to hold other frames
		self.base1 = Frame(self.parent, width=600, height=500, bd = 1, relief = GROOVE)
		self.base1.pack(padx = 5, pady = 5)

		#create second frame
		self.myContainer2 = Frame(self.base1, width=600, height=100)
		self.myContainer2.pack(padx = 5, pady = 20)

		#generate random fractions, operator, and answer to the expression
		self.random_fraction_data = self.generate_fractions()
		self.frac1 = self.random_fraction_data[0]
		self.frac2 = self.random_fraction_data[1]
		self.op = self.random_fraction_data[2]
		self.correct_answer = self.random_fraction_data[3]
		#FIXME: refer to bug noted in check_Answer function
		self.users_answer_final = StringVar()

		#instructional text for the user
		self.name = Label(self.myContainer2, text="What is the reduced form of this expression?",  height = 3, width = 72, font=(25))
		self.name.pack(anchor=CENTER)

		#create a third frame
		self.myContainer3 = Frame(self.base1, width=600, height=400)
		self.myContainer3.pack(padx = 5, pady = 10)

		#display both fractions and the operator
		self.fraction1 = Label(self.myContainer3, text=self.frac1, font=(40))
		self.fraction1.grid(row = 0, column = 0)
		self.operator = Label(self.myContainer3, text=self.op, font=(40))
		self.operator.grid(row = 0, column = 1)
		self.fraction2 = Label(self.myContainer3, text=self.frac2, font=(40))
		self.fraction2.grid(row = 0, column = 2)

		#instructional text, entry box for user's answer
		self.answer_label = Label(self.myContainer3, text="Answer:", font=(40))
		self.answer_label.grid(row = 4, column = 0, padx = 4, pady=30)
		#FIXME: refer to bug noted in check_Answer function
		self.users_answer = Entry(self.myContainer3, textvariable=self.users_answer_final)
		self.users_answer.grid(row = 4, column = 1)

		#display correct or incorrect
		self.answer_label = Label(self.myContainer3, text="", font=(40))
		self.answer_label.grid(row = 8, column = 0, padx = 10, pady=5)

		#submission button
		self.submit_button = Button(self.myContainer3, height = 2, width = 12)
		self.submit_button["text"] = "Submit"
		self.submit_button.grid(row = 6, column = 0, padx = 10, pady = 5)
		self.submit_button.bind("<Button-1>", self.check_answer)

		#next question button
		self.next_button = Button(self.myContainer3, height = 2, width = 12, bg="lightgrey")
		self.next_button["text"] = "Next Question"
		self.next_button.grid(row = 6, column = 2, padx = 10, pady = 5)
		self.next_button.bind("<Button-1>", self.startQuizzer)

	#input: event object
	#output: 
	#description: presents equation to solve, they pick operator, num and denom, solve button, answer appears
	def startSolver(self, event):
		print("solver initialized...")

		#destroy and resize orginal frame
		self.myContainer1.destroy()
		self.myContainer2.destroy()
		self.parent.minsize(width=700, height=500)

		try:
			self.base1.destroy()
		except:
			print("base1 does not exist")

		#create the navigation bar
		self.navBar()

		#create base frame to hold other frames
		self.base1 = Frame(self.parent, width=600, height=500, bd = 1, relief = GROOVE)
		self.base1.pack(padx = 5, pady = 5)

		#create second frame
		self.myContainer2 = Frame(self.base1, width=600, height=100)
		self.myContainer2.pack(padx = 5, pady = 20)

	#input: event object
	#output: 
	#description: shows, for each operator and all operators, the user's averages vs average for all users
	def startResults(self, event):
		print("results initialized...")

		db = MySQLdb.connect("localhost", "root", "YOURPASS", "fractions_test")
		cursor = db.cursor()
		username_query =  "SELECT * FROM users"
		cursor.execute(username_query)

		results = cursor.fetchall()
		db.close()

		#destroy and resize orginal frame
		self.myContainer1.destroy()
		self.myContainer2.destroy()
		self.parent.minsize(width=700, height=500)

		try:
			self.base1.destroy()
		except:
			print("base1 does not exist")

		#create the navigation bar
		self.navBar()

		#create base frame to hold other frames
		self.base1 = Frame(self.parent, width=600, height=500, bd = 1, relief = GROOVE)
		self.base1.pack(padx = 5, pady = 5)

		r = 0
		c = 0

		Label(self.base1, text="Username", font=(20)).grid(row=r, column=c, padx=5, pady=5)
		Label(self.base1, text="Score", font=(20)).grid(row=r, column=1, padx=5, pady=5)

		for data in results:
			r += 1
			Label(self.base1, text=data[1]).grid(row=r, column=c, padx=5, pady=5)
			Label(self.base1, text=data[3]).grid(row=r, column=c+1, padx=5, pady=5)

	#input: event object
	#output: 
	#description: quit the program
	def quit(self, event):
		print("quitting...")
		self.parent.destroy()

	#FIXME: BUG: self.users_answer is appearing as a set of integers, whereas self.correct_answer is appearing correct
			#BUG FIX: declared stringVar() variable self.users_answers_final, which allows for .get() method to be used
			# this is a patchwork solution, and seems very nasty
	#input: event object, correct answer, user's answer, username
	#output: string
	#description: quit the program
	def check_answer(self, event):
		print("checking answer... user's is:", self.users_answer_final.get(), "correct is: ", self.correct_answer)

		#remove the entry widget, add a label to prevent user from entering again
		self.users_answer.config(state=DISABLED)

		if self.correct_answer == self.users_answer_final.get():
			#update user score in db
			self.alter_score(self.username_master, 1.0)
			print("Correct!")
			self.answer_label['text'] = "Correct!"
		else:
			print("Incorrect! Either your answer was invalid, or it was not formatted correctly!")
			self.answer_label['text'] = "Incorrect!"

	#input: 
	#output: 
	#description: generate random fractions, return fraction1, operator, fraction2, answer
	def generate_fractions(self):
		self.num1 = 0
		self.num2 = 0
		self.denom1 = 0
		self.denom2 = 0

		self.ops_table = {'+': operator.add, '*': operator.mul, '-': operator.sub, '/': operator.truediv}
		self.operations = { 0:'+', 1:'-', 2:'*', 3:'/'}

		while ((self.num1 == 0) or (self.num2 == 0) or (self.denom1 == 0) or (self.denom2 == 0)):
			random.seed()
			self.num1 = random.randint(-10, 10)
			random.seed()
			self.denom1 = random.randint(-10, 10)
			random.seed()
			self.num2 = random.randint(-10, 10)
			random.seed()
			self.denom2 = random.randint(-10, 10)

		print("numerators:", self.num1, self.num2, "denomerators:", self.denom1, self.denom2)

		self.op = self.operations[random.randint(0,3)]


		self.frac_1 = fractions.Fraction(self.num1, self.denom1)
		self.frac_2 = fractions.Fraction(self.num2, self.denom2)

		self.frac_final = self.ops_table[self.op](self.frac_1, self.frac_2)

		return((str(self.frac_1), str(self.frac_2), self.op, str(self.frac_final)))

	#input: event object
	#output: 
	#description: actions for login button
	def loginClick(self, event):
		print("login details:")

		print("username:", self.username.get())
		print("password:", self.password.get())
		logged_in = self.login(self.username.get(), self.password.get())

		if(logged_in['login']):
			print("Beginning code once logged in...")
			self.mainMenu()

	#input: event object
	#output: 
	#description: actions for button2
	def createClick(self, event):
		print("user creation details:")

		print("username:", self.username.get())
		print("password:", self.password.get())
		account_created = self.create_account(self.username.get(), self.password.get())

	#input: username, password to attampt login
	#output: dictionary {'username':username, 'login': True or False, login successful or not}
	#description: user authentication system
	def login(self, username, password):
		print("starting authentication procedure...")

		db = MySQLdb.connect("localhost", "root", "YOURPASS", "fractions_test")
		cursor = db.cursor()
		username_query =  "SELECT * FROM users WHERE username = '%s'" % username
		
		try:
			print("executing query:", username_query)
			cursor.execute(username_query)
			results = cursor.fetchall()
		except Exception as e:
			print("error executing query:", e)
			db.close()
			return {'username':username, 'login':False}

		try:
			if results[0][1] == username:
				print("username found:", results)
				if password == results[0][2]:
					print("password is correct, user logged in")
					db.close()
					self.username_master = username
					return {'username':username, 'login':True}
				else:
					print("password incorrect, user not logged in")
					db.close()
					return {'username':username, 'login':False}
			else:
				print("username %s not found" % (username))
				db.close()
				return {'username':username, 'login':False}
		except:
			print("user does not exist")
			db.close()
			return {'username':username, 'login':False}

	#input: username, password of user to create
	#output: {'username': username, 'created': True or False, whether creation was successful or not}
	#description: user creation
	def create_account(self, username, password):
		print("starting account creation procedure...")

		db = MySQLdb.connect("localhost", "root", "YOURPASS", "fractions_test")
		cursor = db.cursor()
		username_query =  "SELECT * FROM users WHERE username = '%s'" % username
		
		try:
			print("executing query:", username_query)
			cursor.execute(username_query)
			results = cursor.fetchall()
		except Exception as e:
			print("error executing query:", e)
			db.close()
			return {'username':username, 'created':False}

		try:
			if results[0][1] == username:
				print("username already exists:", results)
				db.close()
				return {'username':username, 'created':False}
		except:
			print("user does not exist, proceeding with account creation")
			try:
				insert_statement = "INSERT INTO users(username, password, score) VALUES ('%s', '%s', '%d')" % (username, password, 0)
				cursor.execute(insert_statement)
				print("user %s created" % (username))
				db.commit()
				db.close()
				return {'username':username, 'created':True}
			
			except:
				print("error executing insert statement")
				db.close()
				return {'username':username, 'created':False}	

	#input: username, score to add (double: 1.0 or 0.5)
	#output: 
	#description: alter correct table
	def alter_score(self, username, value):
		db = MySQLdb.connect("localhost", "root", "YOURPASS", "fractions_test")
		cursor = db.cursor()
		insert_statement = "UPDATE users SET score='%d' WHERE username='%s'" % ((self.get_users_score(username) + value), username)

		if value == 1.0:
			print("executing statement:", insert_statement)
			cursor.execute(insert_statement)
			print("score value for user", username, "updated successfully")
			db.close()
		else:
			print("can only add 1.0 or 0.5 points to score")

	#input: username
	#output: 
	#description: get a user's score
	def get_users_score(self, username):
		db = MySQLdb.connect("localhost", "root", "YOURPASS", "fractions_test")
		cursor = db.cursor()
		username_query =  "SELECT * FROM users WHERE username = '%s'" % username

		cursor.execute(username_query)
		results = cursor.fetchall()
		db.close()

		return results[0][3]

root = Tk()
root.minsize(width=700, height=500)
root.wm_title("Fractions Helper")
myapp = MyApp(root)
root.mainloop()