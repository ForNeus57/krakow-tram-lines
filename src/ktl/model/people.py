from random import random, choice
import json
class Person:
  id = None
  def __init__(self, start_stop = '' , end_stop = '' , line = None, time = 0, name_mode='en'):
    self.id = Person.generate_id()
    self.name = Person.generate_name(name_mode)
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
  def generate_name(mode='en'):
    if mode == 'en':
      with open('src\\ktl\\model\\names_info\\first-names.json', 'r', encoding='utf-8') as file:
        first_names = json.load(file)
      with open('src\\ktl\\model\\names_info\\middle-names.json', 'r', encoding='utf-8') as file:
        middle_names = json.load(file)
      with open('src\\ktl\\model\\names_info\\names.json', 'r', encoding='utf-8') as file:
        last_names = json.load(file)
      if random() < 0.1:
        first_name = first_names[int(random() * len(first_names))]
        middle_name = middle_names[int(random() * len(middle_names))]
        last_name = last_names[int(random() * len(last_names))]
        return f"{first_name} {middle_name} {last_name}"
      else:
        first_name = first_names[int(random() * len(first_names))]
        last_name = last_names[int(random() * len(last_names))]
        return f"{first_name} {last_name}"
    elif mode == 'pl':
      with open('src\\ktl\\model\\names_info\\maleNames.json', 'r', encoding='utf-8') as file:
        male_names = json.load(file)
      with open('src\\ktl\\model\\names_info\\femaleNames.json', 'r', encoding='utf-8') as file:
        female_names = json.load(file)
      with open('src\\ktl\\model\\names_info\\maleSurnames.json', 'r', encoding='utf-8') as file:
        male_surnames = json.load(file)
      with open('src\\ktl\\model\\names_info\\femaleSurnames.json', 'r', encoding='utf-8') as file:
        female_surnames = json.load(file)
      if random() < 0.5:
        name = female_names[int(random() * len(female_names))]
        surname = female_surnames[int(random() * len(female_surnames))]
      else:
        name = male_names[int(random() * len(male_names))]
        surname = male_surnames[int(random() * len(male_surnames))]
      return f"{name} {surname}"
    else:
      raise Exception('Mode not supported')

    
  def __repr__(self):
    return f"Person({self.id}, {self.name}, {self.start_stop}, {self.end_stop}, {self.line}, {self.time})"

def generate_people(probability, range, name_mode='en'):
  people = []
  for i in range:
    if random() < probability:
      people.append(Person(name_mode=name_mode))
  return people





