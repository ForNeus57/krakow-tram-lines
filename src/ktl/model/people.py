from random import random
import json
class Person:
  id = None
  def __init__(self):
    self.id = Person.generate_id()
    self.name = Person.generate_name()

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
    return f"Person({self.name})"

def generate_people(probability, range):
  people = []
  for i in range:
    if random() < probability:
      people.append(Person())
  return people

def main():
  people = generate_people(0.5, range(100))
  for person in people:
    print(person.name)

  # check the number of names in files names_info/names.json /first_names and /middle_names



if __name__ == '__main__':
  main()