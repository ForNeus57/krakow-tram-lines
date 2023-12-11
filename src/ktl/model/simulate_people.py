'''
using   data/generated/pickle/tram_stops.pkl
        data/generated/pickle/time_table.pkl

w pętli po czasie
  dla każdego przystanku        
    dla przystanku biorę losową linię, z niej wybieram losowy przystanek i sprawdzam czy jest po nim, jak tak to wpisujemy go dla generowanego person jako tram_stop
TODO
  - person generateNames() eng i pl DONE name_mode = 'en'/'pl' w generate_people(), generate_name(), Person()
  - wypisać które przystanki wywalają błędy DONE erroring_stops.json w data/generated/json
'''
import time

from ktl.model.people import Person, generate_people
from ktl.model.stops import Stop
from random import random, choice
import json
import pandas as pd
from ktl.model.probability import *

tram_stops_pickle = pd.read_pickle('data/generated/pickle/tram_stops.pkl')
time_table_pickle = pd.read_pickle('data/generated/pickle/time_table.pkl')
people_list = []
erroring_stops = []
errors_generating_people = 0


class SimulatePeople:
    time = 0
    probability = 0.03
    stops = []

    def __init__(self, time=700, probability=0.03, stops: Stop = []):
        self.time = time
        self.probability = probability
        self.stops = stops

    def time_step(self):
        global time_table_pickle, tram_stops_pickle, people_list, errors_generating_people, erroring_stops
        self.time += 1

        print(f'time: {self.time}')
        for stop in self.stops:
            number_of_people = 0
            if random() < tram_probability(self.time):
                number_of_people = 1  # will modify later, maybe not.
            for person in range(number_of_people):
                try:
                    person = Person()
                    person.start_stop = stop.stop_name
                    choi = get_line_list_from_train_stops(time_table_pickle, stop.stop_name)

                    choi = choice(list(zip(*choi)))

                    line, direction = choi

                    end_stop = stop.stop_name
                    while end_stop == stop.stop_name:
                        end_stop = choice(get_train_stops_from_line(time_table_pickle, str(line), str(direction)))

                    person.end_stop = end_stop
                    person.line = line
                    person.time = self.time

                    # do kalsy perason dodać kierunek ---- direction

                    stop.people_waiting.append(person)
                    print(f'person: {person}')
                    people_list.append(person)
                except Exception as e:
                    print(f'Error generating person: {e}')
                    errors_generating_people += 1
                    erroring_stops.append(stop.stop_name)

            # something something add people to tram that's not implemented yet, take them off the stop

    def run(self):
        while self.time < 20 * 60:
            self.time_step()
        print('simulation ended', f'errors generating people: {errors_generating_people}')


# wrzucasz przystanek, dostajesz liste linii
def get_line_list_from_train_stops(df, tram_name):
    query: pd.DataFrame = df.groupby('stop_name').get_group(tram_name)

    return query['line'].to_list(), query['direction'].to_list()


# wrzucasz linię, dostajesz liste przystankow
def get_train_stops_from_line(df, line, direction):

    query: pd.DataFrame = df.groupby('line').get_group(line)

    query: pd.DataFrame = query.groupby('direction').get_group(direction)
    # print(line, direction)
    # print(query.to_string())

    return query['stop_name'].tolist()


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

    # run the simulation
    simulate_people = SimulatePeople(7 * 60, 0.03, stops)
    simulate_people.run()

    # save people to json
    people_list_encoded = []
    for person in people_list:
        person_encoded = {
            "id": person.id,
            "name": person.name,
            "start_stop": person.start_stop,
            "end_stop": person.end_stop,
            "line": person.line,
            "time": person.time
        }
        people_list_encoded.append(person_encoded)
    people_json = json.dumps(people_list_encoded, indent=4, ensure_ascii=False)

    with open('data/generated/json/people.json', 'w', encoding='utf-8') as file:
        file.write(people_json)

    # save erroring stops to json, beforehand removing duplicates
    global erroring_stops
    erroring_stops = list(dict.fromkeys(erroring_stops))
    erroring_stops_json = json.dumps(erroring_stops, indent=4, ensure_ascii=False)
    with open('data/generated/json/erroring_stops.json', 'w', encoding='utf-8') as file:
        file.write(erroring_stops_json)


if __name__ == '__main__':
    main()

    # print(get_line_list_from_train_stops(time_table_pickle, ''))
