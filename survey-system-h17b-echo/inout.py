import csv
from abc import abstractmethod, ABCMeta
class Reader(metaclass=ABCMeta):

   @abstractmethod
   def read(f):
      pass

class Writer(metaclass=ABCMeta):
   
   @abstractmethod
   def write(f, row):
      pass

class CSVReader(Reader):
   
   def read(self, f):
      results = []
      with open(f,'r') as csv_in:
         reader = csv.reader(csv_in)
         for row in reader:
            results.append(row)
         return results


class CSVWriter(Writer):
   
   def write(self, f, row):
      with open(f,'a') as csv_out:
         writer = csv.writer(csv_out)
         writer.writerow(row)


      
