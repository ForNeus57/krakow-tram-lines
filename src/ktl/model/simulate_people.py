'''
wczytać data/generated/pickle/tram_stops.pkl
        data/generated/pickle/time_table.pkl

w pętli po czasie
  dla każdego przystanku        
    dla przystanku biorę losową linię, z niej wybieram losowy przystanek i sprawdzam czy jest po nim, jak tak to wpisujemy go dla generowanego person jako tram_stop


'''
from ktl.model.people import Person, generate_people
from ktl.model.stops import Stop
from random import random, choice
import json
import pandas as pd

tram_stops_pickle = pd.read_pickle('data/generated/pickle/tram_stops.pkl')
time_table_pickle = pd.read_pickle('data/generated/pickle/time_table.pkl')
people_list = []

class SimulatePeople:
  time = 7 * 60
  probability = 0.03
  stops = []

  def __init__(self, time = 700, probability = 0.03, stops: Stop = []):
    self.time = time
    self.probability = probability
    self.stops = stops
    
  def time_step(self):
    global time_table_pickle, tram_stops_pickle, people_list
    self.time += 1

    print(f'time: {self.time}')  
    for stop in self.stops:
      number_of_people = 0
      if random() < self.probability:
        number_of_people = 1 # will modify later
      for person in range(number_of_people):
        try:
          person = Person()
          person.start_stop = stop.stop_name
          line = choice(get_line_list_from_train_stops(time_table_pickle, stop.stop_name))
          end_stop = stop.stop_name
          while end_stop == stop.stop_name:
            end_stop = choice(get_train_stops_from_line(time_table_pickle, f'{line}'))


          person.end_stop = end_stop
          person.line = line
          person.time = self.time
          stop.people_waiting.append(person)
          print(f'person: {person}')
          people_list.append(person)
        except Exception as e:
          print(f'Error generating person: {e}')

      # something something add people to tram that's not implemented yet, take them off the stop

  def run(self):
    while self.time < 20*60:
      self.time_step()
    print('simulation ended')

#wrzucasz przystanek, dostajesz liste linii
def get_line_list_from_train_stops(df, tram_name):
  return df.groupby('name').get_group(tram_name)['line'].tolist()

#wrzucasz linię, dostajesz liste przystankow
def get_train_stops_from_line(df, line):
  return df.groupby('line').get_group(line)['name'].tolist()

def main():
  global tram_stops_pickle 
  global time_table_pickle 
  stops = []
  stop_id = 0

  # get all stops from tram_stops_pickle
  for idx, row in tram_stops_pickle.iterrows():
    stop_id += 1
    stop_name = row['name']
    people_waiting = []
    stops.append(Stop(stop_id, stop_name, people_waiting))

  
  # print(stops)

  # print(get_line_list_from_train_stops(time_table_pickle, 'Wesele 01'))
  print(get_train_stops_from_line(time_table_pickle, '1'))

  simulate_people = SimulatePeople(700, 0.03, stops)
  simulate_people.run()

  print(people_list)


  people_json = json.dumps([person.__dict__() for person in people_list], indent=4)
  with open('data/generated/json/people.json', 'w') as file:
    file.write(people_json)

#DEBBUGING
  # time = 700
  # print(f'time: {time}')
  # stop = choice(stops)
  # print(f'stop: {stop}, name: {stop.stop_name}')
  # person = Person()
  # print(f'person: {person}')
  # person.start_stop = stop.stop_name
  # print(f'person: {person}')
  # line = choice(get_line_list_from_train_stops(time_table_pickle, stop.stop_name))
  # print(f'line: {line}')
  # try:
  #   end_stop = choice(get_train_stops_from_line(time_table_pickle, f'{line}'))
  # except Exception as e:
  #   print(f'Error generating person: {e}')
  # print(f'end_stop: {end_stop}')
  # person.end_stop = end_stop
  # person.line = line
  # person.time = time
  # stop.people_waiting.append(person)
  # print(f'person: {person}')
#DEBBUGING




if __name__ == '__main__':
  main()