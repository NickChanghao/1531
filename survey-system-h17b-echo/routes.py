#handles routing
#Want to make login a dialogue instead of a different page
from flask import Flask, redirect, render_template, request, url_for
from server import app, check_auth, check_password, questions, surveys, reader, writer, scntrl, smodel, sview, author
from question import Question, Response
from survey import Survey
import csv


@app.before_first_request
def load():
   author.load_db(reader, 'passwords.csv')
   scntrl.load_db(reader)
   #quests = questions.read_questions(reader)
   #print(quests[0][0])
   #questions.gen_questions(quests)
   #survs = surveys.read_surveys(reader)
   #print("boom")
   #surveys.gen_surveys(survs, questions)
   #print("boom2")



#test sessions
@app.route("/test", methods=["GET", "POST"])
def test():
   data = scntrl.available_offerings()
   return render_template("courseSelection.html", data=data)

#test create questions
@app.route("/test1", methods=["GET", "POST"])
def test1():
   if request.method == "POST":
      question = request.form["question"]
      mandatory = int(request.form["man"])
      scntrl.create_question(question, mandatory)
   return render_template("createQ.html");

#test view question pool
@app.route("/test2", methods=["GET", "POST"])
def test2():
   if request.method == "POST":
      question_id = int(request.form["rem"])
      scntrl.remove_question(question_id);
        
   man_questions = scntrl.man_questions()
   opt_questions = scntrl.opt_questions()
   return render_template("Questions.html", man_questions=man_questions, opt_questions=opt_questions);

#test create survey
#is redirected to based on a link an admin clicks
@app.route("/test3/<course_id>", methods=["GET", "POST"])
def test3(course_id):
   if request.method == "POST":
      #process the creation of a new survey
      #max method could be problematic. may be better to have course offering id in survey table
      survey_id = scntrl.create_survey()
      scntrl.update_offering(int(course_id), survey_id)
      quests = request.form.getlist("quest")
      for quest in quests:
         scntrl.add_survey_data(survey_id, int(quest))
      return redirect(url_for('test'))

   course = scntrl.get_offering(int(course_id))
   man_questions = scntrl.man_questions()
   opt_questions = scntrl.opt_questions()
   return render_template("adminCreateSurvey.html", course=course, man_questions=man_questions, opt_questions=opt_questions)


@app.route("/<usr_id>", methods=["GET", "POST"])
def dash(usr_id):
   msg = ''
   if request.method == "POST":
      msg = authenticate()
      author.authenticate()
      return redirect(url_for('dash'), usr_id=authed_id)
   role = author.check_auth(usr_id)
   #if not check_auth():
   if role == 'invalid':
      return sview.login(msg)
   if role == "admin":
      return sview.adash('', '', '')
   elif role == "staff":
      return scntrl.staff_dash(usr_id)
   else:
      return scntrl.student_dash(usr_id)
   #return scntrl.




#maybe its better to obviscate the action from the url i.e url doesn't contain

@app.route("/<usr_id>/CreateSurvey", methods=["GET", "POST"])
def course_offerings(usr_id):
   #should be a user sitting in server
   user = author.curr_user()
   if request.method == "POST":
      #if the requested user action doesn't match then initiate login get login info
      pass
      if author.check_auth(usr_id) == 'invalid':
         pass
         #get login info
   #should probably be just contained in the authentication module
   if author.check_auth(usr_id) == 'invalid':
      return render_template("login.html")
   offerings = scntrl.get_offerings()
   return scntrl.show_offerings(offerings)
      
         

@app.route("/<usr_id>/CreateSurvey/<surv_id>", methods=["GET", "POST"])
def create_survey2(usr_id, surv_id):
   pass
   #check authentication
   #make sure survey to be created is valid

@app.route("/<usr_id>/Questions", methods=["GET", "POST"])
def question_pool(usr_id):
   msg = ''
   user = author.curr_user()
   if request.method == "POST":
      name = scntrl.get_form_data('name')
      password = scntrl.get_form_data('password')
      author.authenticate(name, password)
      if user.get_role() == 'invalid':
         msg = 'Invalid Authentication'
   if author.check_auth(usr_id) == 'invalid':
      return render_template("login.html")

@app.route("/<usr_id>/<survey>", methods=["GET", "POST"])
def survey(user_id, survey):
   if method == "POST":
      pass  
   if user == student:
      return scntrl.get_survey(survey)
   

@app.route("/", methods=["GET", "POST"])
def index():
   msg = ''
   user = author.curr_user()
   if request.method == "POST":
      #msg = authenticate()
      creds = scntrl.get_creds('name', 'password')
      author.authenticate(creds[0], creds[1])
      if user.get_role() == 'invalid':
         msg = 'Invalid Authentication'
   #if not check_auth():
   if user.get_role() == 'invalid':
      return render_template("login.html", msg=msg)
   return redirect(url_for('dash', usr_id=user.get_id()))


#need a solution for differentiating between login and function post requests
#could have one universal login function that redirects instead of having a bunch of if
#statements in each function doing the same thing.
#would require a dedicated login page url
#would need to save the url for the page that initiated the login.
@app.route("/CreateQuestions", methods=["GET", "POST"])
def create_questions():
   msg = ''
   msg2 = ''
   if request.method == "POST":
      if not check_auth():
         msg = authenticate()
      else:
         question = request.form["question"]
         responses = request.form.getlist("ans")
         #quest_obj = make_question(question)
         quest_obj = Question(question, responses)
         #add_responses(quest_obj, responses)
         questions.add_question(quest_obj)
         questions.write_question(quest_obj, writer)
   if not check_auth():
      return render_template("login.html", msg=msg)
   return render_template("createQ.html")

@app.route("/CreateSurvey", methods=["GET", "POST"])
def create_survey():
   global questions
   global surveys
   msg = ''
   if request.method == "POST":
      if not check_auth():
         msg = authenticate()
      else:
         #get form data
         title = request.form["title"]
         desc = request.form["desc"]
         quests = request.form.getlist("quest")
         #print(questions)
         quests = questions.get_subset(quests)
         survey = Survey(title, desc, quests)
         surveys.add_survey(survey)
         surveys.write_survey(survey, writer)
   if not check_auth():
      return render_template("login.html", msg=msg)
   quests = questions.get_questions()
   courses = reader.read("courses.csv")
   #print(courses[0])
   courses = courses[1:]
   return render_template("createS.html", questions=quests, courses=courses)

@app.route("/Survey/<key>", methods=["GET", "POST"])
def load_survey(key):
   survey = surveys.get_survey(key)
   if request.method == "POST":
      #get the data from submitted survey
      bound = len(survey.get_questions())
      i = 0
      row = ''
      answers = []
      while i < bound:
         word = "resp" + str(i+1)
         j = str(int(request.form[word]) - 1)
         answers.append(j)
         i += 1
      writer.write(key+".csv", answers)
   return render_template("survey.html", survey=survey)

@app.route("/Links", methods=["GET", "POST"])
def links():
   return render_template("links.html", surveys=surveys.get_surveys())

#should make it so this function does everything
def authenticate():
   msg = ''
   user_name = request.form["name"]
   password = request.form["password"]
   if not check_password(user_name, password):
      msg = 'Invalid Authentication'
   return msg



