#handles server logic
#need to make more OO coherent
from flask import Flask
from question import Question, Response, Questions
from survey import Survey, Surveys
from inout import CSVReader, CSVWriter
from MVC import SurveyView, SurveyModel, SurveyController
from auth import Authenticator, User
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

admins = {"admin":"password"}
auth = False

questions = Questions()
surveys = Surveys()

reader = CSVReader()
writer = CSVWriter()

sview = SurveyView()
smodel = SurveyModel()
scntrl = SurveyController(smodel, sview)

author = Authenticator(User('', 'invalid'))

def check_auth():
   global auth
   return auth

def check_password(user_name, password):
   global auth
   global admins
   if user_name in admins:   
      if password == admins[user_name]:
         auth = True
   return auth    
