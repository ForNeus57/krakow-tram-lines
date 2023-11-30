from random import random, choice
import json
class Person:
  id = None
  def __init__(self, start_stop = '' , end_stop = '' , line = None, time = 0):
    self.id = Person.generate_id()
    self.name = Person.generate_name()
    self.start_stop = start_stop
    self.end_stop = end_stop
    self.line = line
    self.time = time

  def __dict__(self):
    return {
      'id': self.id,
      'name': self.name,
      'start_stop': self.start_stop,
      'end_stop': self.end_stop,
      'line': self.line,
      'time': self.time
    }
  
  @staticmethod
  def generate_id():
    if Person.id is None:
      Person.id = 0
    else:
      Person.id += 1
    return Person.id
  
  @staticmethod
  def generate_name():
    with open('src\\ktl\\model\\names_info\\first-names.json', 'r') as file:
      first_names = json.load(file)
    with open('src\\ktl\\model\\names_info\\middle-names.json', 'r') as file:
      middle_names = json.load(file)
    with open('src\\ktl\\model\\names_info\\names.json', 'r') as file:
      names = json.load(file)
    first_name = first_names[int(random() * len(first_names))]
    middle_name = middle_names[int(random() * len(middle_names))]
    name = names[int(random() * len(names))]
    if random() < 0.1:
      return f"{first_name} {middle_name} {name}"
    else:
      return f"{first_name} {middle_name}"
    
  def __repr__(self):
    return f"Person({self.id}, {self.name}, {self.start_stop}, {self.end_stop}, {self.line}, {self.time})"

def generate_people(probability, range):
  people = []
  for i in range:
    if random() < probability:
      people.append(Person())
  return people





