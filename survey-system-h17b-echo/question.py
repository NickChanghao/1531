from inout import CSVWriter, CSVReader

class Question(object):
   def __init__(self, id, question, responses):
      super(Question, self).__init__()
      self.__id = id
      self.__question = question
      self.__responses = self.__gen_responses(responses)
   
   def add_response(self,response):
      self.__responses.append(response)

   def get_responses(self):
      return self.__responses
   
   def get_number(self):
      return self.__number

   def get_id(self):
      return self.__id

   def __gen_responses(self, responses):
      resp_objs = []
      for response in responses:
         print(response)
         resp_objs.append(Response(response))
      return resp_objs
   
   def __str__(self):
      return self.__question

class Response(object):
   def __init__(self, response):
      super(Response, self).__init__()
      self.__response = response
   
   def __str__(self):
      return self.__response

class Questions(object):
   def __init__(self):
      super(Questions, self).__init__()
      self.__qlist = []
      self.__qmap = dict()

   def get_questions(self):
      return self.__qlist

   def get_subset(self, questions):
      quests = []
      for question in questions:
         print(question)
         quests.append(self.get_question(question))
      return quests

   def get_question(self, key):
      print(key)
      if key in self.__qmap:
         print("Hi")
      return self.__qmap.get(key)

   def add_question(self, question):
      if question.__str__() not in self.__qmap:
         self.__qmap.update({question.__str__(): question})
         self.__qlist.append(question)
         return True
      return False

   def gen_questions(self, questions):
      for question in questions:
         print(question[0])
         self.add_question(Question(question[0], question[1:]))


   def write_question(self, question, writer):
      to_write = [question.__str__()]
      for response in question.get_responses():
         to_write.append(response.__str__())
      writer.write("questions.csv", to_write)

   def read_questions(self,reader):
      return reader.read("questions.csv")








