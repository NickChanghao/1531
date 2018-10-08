class Course(object):
   def __init__(self, id, course, session):
      super(Course, self).__init__()
      self.__id = id;
      self.__course = course
      self.__session = session

   def get_id(self):
      return self.__id;
   def get_course(self):
      return self.__course
   def get_session(self):
      return self.__session

class Courses(object):
   def __init__(self, session):
      super(Courses, self).__init__()
      self.__session = session
      self.__courses = []

   def add_course(self, course):
      self.__courses.append(course)

   def get_session(self):
      return self.__session

   def get_courses(self):
      return self.__courses
