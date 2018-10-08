from inout import CSVReader
import sqlite3


class Authenticator(object):
   def __init__(self, user):
      super(Authenticator, self).__init__()
      self.__user = user

   def load_db(self, reader, f):
      records = reader.read(f)
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         for record in records:
            try:
               cursorObj.execute('INSERT INTO USER (ID,PASSWORD,ROLE) VALUES (?,?,?)', (int(record[0]),record[1],record[2],))
               connection.commit()
            except sqlite3.IntegrityError:
               print("already in database")
         try:
            cursorObj.execute('INSERT INTO USER (ID,PASSWORD,ROLE) VALUES (?,?,?)', (1917,"Mandelbrot","admin",))
            connection.commit()
         except sqlite3.IntegrityError:
            print("already in database")
         cursorObj.close()

   def authenticate(self, user_id, password):
      results = []
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         rows = cursorObj.execute('SELECT ROLE FROM USER WHERE ID = ? AND PASSWORD = ?', (user_id, password,))
         connection.commit()
         for row in rows:
            results.append(row)
         cursorObj.close()
      if results:
         self.__user.update_user_id(user_id)
         self.__user.update_role(results[0][0])
      #return results[0][0]

   def check_user(self, user_id):
      return user_id == self.__user.get_id()

   def check_auth(self, user_id):
      if self.check_user(user_id):
         return self.__user.get_role()
      else:
         return 'invalid'

   def curr_user(self):
      return self.__user

class User(object):
   def __init__(self, user_id, role):
      super(User, self).__init__()
      self.__user_id = user_id
      self.__role = role

   def get_id(self):
      return self.__user_id

   def get_role(self):
      return self.__role

   def update_user_id(self, user_id):
      self.__user_id = user_id

   def update_role(self, role):
      self.__role = role

def load_db(reader, f):
   records = reader.read(f)
   with sqlite3.connect('survey.db') as connection:
      cursorObj = connection.cursor()
      for record in records:
         cursorObj.execute('INSERT INTO USER (ID,PASSWORD,ROLE) VALUES (?,?,?)', (int(record[0]),record[1],record[2],))
         connection.commit()
      cursorObj.execute('INSERT INTO USER (ID,PASSWORD,ROLE) VALUES (?,?,?)', (1917,"Mandelbrot","admin",))
      connection.commit()
      cursorObj.close()

def authenticate(user_id, password):
   results = []
   with sqlite3.connect('survey.db') as connection:
      cursorObj = connection.cursor()
      rows = cursorObj.execute('SELECT ROLE FROM USER WHERE ID = ? AND PASSWORD = ?', (user_id, password,))
      connection.commit()
      for row in rows:
         results.append(row)
      cursorObj.close()
   return results[0][0]
      
