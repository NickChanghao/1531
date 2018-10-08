from flask import Flask, render_template, redirect, url_for, request
from inout import CSVReader
from courses import Course, Courses
from question import Question
import sqlite3

class SurveyController(object):
   def __init__(self, model, view):
      super(SurveyController, self).__init__()
      self.__model = model
      self.__view = view
      #self.__log_redirect = log_redirect



   def load_db(self, reader):
      self.__model.load_courses(reader, "courses.csv")
      self.__model.load_connections(reader, "enrolments.csv")

   #def go_redirect(self):
    #  return redirect(url_for(redirect[]))

   def student_dash(self, student):
      open_surveys = self.__model.get_open_surveys(student)
      closed_surveys = self.__model.get_closed_surveys(student)
      return self.__view.rdash(open_surveys, closed_surveys)

   def staff_dash(self, staff):
      pass
   
   def update_offering(self, course_id, survey_id):
      self.__model.update_offering(course_id, survey_id)

   def admin_dash(self):
      pass

   def create_survey(self):
      return self.__model.create_survey()

   def get_offering(self, id):
      return self.__model.get_offering(id)

   def create_question(self, question, mandatory):
      self.__model.create_question(question, mandatory)

   def available_offerings(self):
      return self.__model.get_offerings()

   def get_survey(self, survey):
      survey = self.__model.get_survey(survey)
      #return self.__view.

   def add_submission(self, submission):
      pass

   def man_questions(self):
      return self.__model.get_man_questions()

   def opt_questions(self):
      return self.__model.get_opt_questions()

   def get_form_data(self, element):
      return request.form[element]
   
   def add_survey_data(self, survey_id, question_id):
      self.__model.add_survey_data(survey_id, question_id)

   def remove_question(self, question_id):
      self.__model.remove_question(question_id)

   def get_creds(self, name, password):
      creds = []
      creds.append(request.form[name])
      creds.append(request.form[password])
      return creds

class SurveyModel(object):
   #def __init__(self)
   #could probs make a function with the 
   def load_courses(self, reader, f):
      records = reader.read(f)
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         for record in records:
            try:
               cursorObj.execute('INSERT INTO COURSE_OFFERING (COURSE, SESSION) VALUES (?,?)', (record[0], record[1]))
               connection.commit()
            except sqlite3.IntegrityError:
               print("already in database")
         cursorObj.close()
   
   #should do a check and put into singular tables
   def load_connections(self, reader, f):
      records = reader.read(f)
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         for record in records:
            try:
               cursorObj.execute('INSERT INTO USER_COURSE (USER_ID, COURSE_ID, SEEN) VALUES (?,?,?)', (record[0], record[1], 0))
               connection.commit()
            except sqlite3.IntegrityError:
               print("already in database")
         cursorObj.close()


   def get_in_review(self):
      data = self.__db_query('')

   def get_survey(self, survey):
      pass
   
   def create_survey(self):
      return self.__db_insert('INSERT INTO SURVEY DEFAULT VALUES', ())   

   def create_question(self, question, mandatory):
      self.__db_insert('INSERT INTO QUESTION (QUEST, MANDATORY, STATUS) VALUES (?,?,?)',(question, int(mandatory), 1))

   def add_survey_data(self, survey_id, question_id):
      self.__db_insert('INSERT INTO SURVEY_DATA (SURVEY_ID, QUESTION_ID) VALUES (?,?)', (survey_id, question_id))


   #these functions are really similar   
   def get_man_questions(self):
      data = self.__db_query('SELECT ID, QUEST FROM QUESTION WHERE MANDATORY = ? AND STATUS = ?', (1,1))
      questions = []
      for record in data:
         questions.append(Question(record[0], record[1], []))
      return questions
   
   def get_opt_questions(self):
      data = self.__db_query('SELECT ID, QUEST FROM QUESTION WHERE MANDATORY = ? AND STATUS = ?', (0,1))
      questions = []
      for record in data:
         questions.append(Question(record[0], record[1], []))
      return questions

   def remove_question(self, question_id):
      self.__db_update('UPDATE QUESTION SET STATUS = ? WHERE ID = ?', (0, question_id))

   def get_sessions(self, order=''):
      return self.__db_query('select distinct session from course_offering where survey_id is null', ())
   
   def get_offerings_by_session(self, session, order=''):
      pass
      #offerings =

   def get_offerings(self):
      offerings = self.__db_query('SELECT ID, COURSE, SESSION FROM COURSE_OFFERING WHERE SURVEY_ID IS NULL ORDER BY SESSION, COURSE ASC', ())
      data = []
      seen = ''
      #courses = []      
      for offering in offerings:
         #courses = ''
         if offering[2] != seen:
            print('seen')
            seen = offering[2]
            courses = Courses(offering[2])
            data.append(courses)
            #data.append(offering[1])
            #courses = []
            #data.append(courses)
         courses.add_course(Course(offering[0], offering[1], offering[2]))
         #courses.append(offering)
      return data

   def get_offering(self, id):
      #what happens if given id doesn't match the query
      data = self.__db_query('SELECT ID, COURSE, SESSION FROM COURSE_OFFERING WHERE ID = ? AND SURVEY_ID IS NULL', (id,))
      print(data)
      for dat in data:
         print(dat)
      return Course(data[0][0], data[0][1], data[0][2])
      
   def update_offering(self, course_id, survey_id):
      self.__db_update('UPDATE COURSE_OFFERING SET SURVEY_ID = ? WHERE ID = ?', (survey_id, course_id))   

   def get_open_surveys(self, user):
      return self.__db_query('SELECT COURSE, SESSION FROM PLACEHOLDER WHERE USER = ? AND ')
   
   def get_closed_surveys(self, user):
      pass

   def get_survey_results(self, user):
      pass

   def get_areviews(self):
      pass

   def get_sreviews(self, user):
      pass

   def add_response(self, survey, question, answer):
       self.__db_insert('INSERT INTO RESPONSES (?,?,?)', (survey, question, answer,))

   def __db_query(self, query, payload):
      results = []
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         rows = cursorObj.execute(query, payload)
         connection.commit()
         for row in rows:
            results.append(row)
         cursorObj.close()
      return results
      
   def __db_update(self, statement, payload):
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         cursorObj.execute(statement, payload)
         connection.commit()
         cursorObj.close()

   def __db_insert(self, statement, payload):
      with sqlite3.connect('survey.db') as connection:
         cursorObj = connection.cursor()
         cursorObj.execute(statement, payload)
         connection.commit()
         id = cursorObj.lastrowid
         cursorObj.close()
      return id

class SurveyView(object):

   def login(self, msg):
      return render_template("login.html", msg=msg)
   
   def rdash(self, data):
      return render_template("rdash.html", data=data)

   def sdash(self):
      pass

   def adash(self, surveys, reviews, questions):
      return render_template("adash.html", surveys=surveys, reviews=reviews, questions=questions)

   def fill_survey(self, survey):
      return render_template("survey.html", survey=survey)
   
