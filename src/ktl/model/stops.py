from random import random
import json

class Stop:
    def __init__(self, stop_id, stop_name, people_waiting = []):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.people_waiting = people_waiting
        
    def __repr__(self):
        return f"Stop({self.stop_id}, {self.stop_name}, {self.people_waiting})"
    
    def add_people(self, people_waiting):
        for person in people_waiting:
          self.people_waiting.append(person)
    
    def remove_people(self, people):
        for person in people:
          self.people_waiting.remove(person)


