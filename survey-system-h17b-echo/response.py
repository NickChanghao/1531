class Response(object):
   def __init__(self, response):
      super(Response, self).__init__()
      self.__response = response
   
   def __str__(self):
      return self.__response
