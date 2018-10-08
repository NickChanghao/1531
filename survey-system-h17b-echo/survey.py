#maybe have a questions wrapper type so you can do an add question without knowing
#implementation
#maybe make your own collection type and use for questions and responses
#should the key be in the class??
from inout import CSVReader, CSVWriter

class Survey(object):
   
   def __init__(self, title, desc='', questions=None, key=''):
      super(Survey, self).__init__()
      self.__title = title
      self.__desc = desc
      self.__key = key
      self.__questions = []
      if questions is not None:
         self.__questions = questions
      
      
   def add_key(self, key):
      self.__key = str(key)   

   def add_question(self, question):
      self.__questions.append(question)

   def get_title(self):
      return self.__title
   
   def get_desc(self):
      return self.__desc

   def get_questions(self):
      return self.__questions

   def get_key(self):
      return self.__key


class Surveys(object):

   def __init__(self):
      self.__smap = dict()
      self.__key = 0

   def get_survey(self, key):
      return self.__smap.get(key)

   def add_survey(self, survey):
      if survey.get_key() not in self.__smap:
         survey.add_key(self.__key)
         self.__key += 1
         self.__smap.update({survey.get_key(): survey})
         return True
      return False

   def get_surveys(self):
      return list(self.__smap.values())

   def gen_surveys(self, survs, questions):
      for surv in survs:
         i = 3
         print(surv[2])
         print(surv[3])
         quests = []
         while i < len(surv):
            quests.append(questions.get_question(surv[i]))
            i += 1
         self.add_survey(Survey(surv[1],surv[2], quests, surv[0]))

   def read_surveys(self, reader):
      return reader.read("surveys.csv")   
   
   def write_survey(self, survey, writer):
      to_write = [survey.get_key(), survey.get_title(), survey.get_desc()]
      for question in survey.get_questions():
         to_write.append(question.__str__())
      writer.write("surveys.csv", to_write)

