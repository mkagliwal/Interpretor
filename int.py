class Program:
	def __init__(self,characters):
		self.dictionary={}
		self.L=CompoundStatement(characters,self.dictionary).function()
	def run(self):
		for i in range(len(self.L)):
			self.L[i].run(self.dictionary)
	def __str__(self):
		return str(self.dictionary)

class CompoundStatement:
	def  __init__(self,statement,dictionary):
		self.L=[]
		statement=statement.rstrip()
		while len(statement)>0:
			statement=statement.lstrip()
			if statement.startswith("while"):
				temps=while_Statement(statement,dictionary)
				temp,statement=temps.function()
				self.L += [temps]
			elif statement.startswith("if"):
				temps=if_Statement(statement,dictionary)
				temp,statement=temps.function()
				self.L += [temps]
			else:
				temps=Statement(statement,dictionary)
				temp,statement=temps.function()
				self.L += [temps]
	def function(self):
		return self.L

class Statement:
	def __init__(self,statement,dictionary):
		self.i=statement.find(";")
		self.State=statement[0:self.i]
		statement=statement[self.i+1:]
		self.remain=statement
	def function(self):
		return self.State, self.remain
	def run(self,dictionary):
		self.State=Assign(self.State,dictionary)

class while_Statement:
	def __init__(self,statement,dictionary):
		self.flag=0
		for i in range(1,len(statement)):
			self.word=statement[i:]
			if self.word.startswith("while"):
				self.flag=self.flag+1
			if self.word.startswith("done"):
				if self.flag==0:
					break
				else:
					self.flag=self.flag-1
		self.State=statement[0:i]
		statement=statement[i+4:]
		self.remain=statement
	def function(self):
		return self.State, self.remain
	def comp(self):
		i=self.State.find("do")
		self.cond=self.State[5:i]
		h=self.State[i+2:]
		h=CompoundStatement(h,dictionary)
		self.variant=h.function()
    	def run(self,dictionary):
    		self.comp(dictionary)
    		self.cond=self.cond.replace(" ","")
    		self.cond=Condn(self.cond,dictionary)
    		while self.cond.Condn_eval(dictionary):
    			for i in range(len(self.variant)):
	    			self.variant[i].run(dictionary)	

class if_Statement:
	def __init__(self,statement,dictionary):
		self.flag=0
		for i in range(1,len(statement)):
			self.word=statement[i:]
			if self.word.startswith("if"):
				self.flag=self.flag+1
			if self.word.startswith("fi"):
				if self.flag==0:
					break
				else:
					self.flag=self.flag-1
		self.State=statement[0:i]
		statement=statement[i+2:]
		self.remain=statement
	def function(self):
		return self.State, self.remain

class Assign:
	def __init__(self,characters,dictionary):
		characters=characters.replace(" ","")
		self.left,self.right=characters.split(":=")
		self.right=expr(self.right,dictionary)
		dictionary[self.left]=self.right.eval(dictionary)

class expr:
	def __init__(self,characters,dictionary):
		self.characters=characters
	def eval(self,dictionary):
		self.characters.replace(" ","")
		if "+" in self.characters:
			self.left,self.right=self.characters.split("+")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			return self.left+self.right
		elif "-" in self.characters:
			self.left,self.right=self.characters.split("-")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			return self.left-self.right
		elif "*" in self.characters:
			self.left,self.right=self.characters.split("*")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			return self.left*self.right
		elif "/" in self.characters:
			self.left,self.right=self.characters.split("/")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			return self.left/self.right
		elif self.characters.replace(".", "").isdigit():
			return float(self.characters)
		elif self.characters.replace("-", "").isdigit():
			l=-int(self.characters.replace("-", ""))
			return l
		else:
			return dictionary[self.characters]

class Condn:
	def __init__(self,characters,dictionary):
		self.characters=characters
	def Condn_eval(self,dictionary):
		if "<=" in self.characters:
			self.left,self.right=self.characters.split("<=")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			if self.left<=self.right:
				return True
			else:
				return False
		elif ">=" in self.characters:
			self.left,self.right=self.characters.split(">=")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			if self.left>=self.right:
				return True
			else:
				return False
		elif "!=" in self.characters:
			self.left,self.right=self.characters.split("!=")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			if self.left!=self.right:
				return True
			else:
				return False
		elif "=" in self.characters:
			self.left,self.right=self.characters.split("=")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			if self.left==self.right:
				return True
			else:
				return False
		elif ">" in self.characters:
			self.left,self.right=self.characters.split(">")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			if self.left>self.right:
				return True
			else:
				return False
		elif "<" in self.characters:
			self.left,self.right=self.characters.split("<")
			self.left=expr(self.left,dictionary)
			self.right=expr(self.right,dictionary)
			self.left=self.left.eval(dictionary)
			self.right=self.right.eval(dictionary)
			if self.left<self.right:
				return True
			else:
				return False

F=open("test.py", "r")
num=F.read()
F.close()
numb=Program(num)
numb.run()
print numb

		





