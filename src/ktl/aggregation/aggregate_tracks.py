import pickle
import networkx as nx
import json
import matplotlib.pyplot as plt
import osmnx as ox
import taxicab as tc

from pathlib import Path

import pandas as pd
import re
import osmnx as ox


pass
# def aggregate_tracks():
#   # Load tracks.pkl
#   tracks = None
#   with open('./data/generated/pickle/tracks.pkl', 'rb') as f:
#     tracks = pickle.load(f)


#   df_stops = pd.read_excel('data/generated/excel/tram_stops.xlsx')
#   df_time = pd.read_excel('data/generated/excel/time_table.xlsx')
#   merged = pd.merge(df_stops, df_time, on='name', how='inner')
    

#   merged = merged[['name', 'geometry','line','order']]

#   tram_stops = {}
  
#   for index, row in merged.iterrows():
#       line = row['line']
#       order = row['order']
#       if row['name'][-2:].strip().isdigit():
#           stop_name = row['name'][:-3].strip()
#           stop_nr = row['name'][-2:].strip()
#       else:
#           stop_name = row['name'].strip()
#           stop_nr = ''
      
#       geometry = row['geometry']
#       match = re.match(r"POINT \(([\d.]+) ([\d.]+)\)", geometry)
#       if match:
#           x = float(match.group(1))
#           y = float(match.group(2))
#           stop_position = (x, y)
#       else:
#           x = None
#           y = None
      
#       tram_stop = (line, order, stop_name, stop_nr, stop_position)
      
#       if '' in tram_stops:
#           tram_stops[''].append(tram_stop)
#       else:
#           tram_stops[''] = [tram_stop] 

#  # print(tram_stops)
#  # print(type(tram_stops))

#  # for line, stops in tram_stops.items():
#   #  print(f"Line: {line}")
#   #  for stop in stops:
#    #   print(f"{stop[0]} {stop[1]} {stop[2]} {stop[3]} {stop[4]}")

  
#   line_coordinates = {}

#   for line, stops in tram_stops.items():
#     for stop in stops:
#       line = stop[0]
#       coordinates = stop[4]
#       if line not in line_coordinates:
#         line_coordinates[line] = []
#       line_coordinates[line].append(coordinates)

#   routes = {}
#   G = tracks
#   for line, coordinates in line_coordinates.items():
#     print(f"Line: {line, coordinates}")
#     track = nx.Graph()
#     for i in range(len(coordinates)-1):
#       orig = (float("{:.3f}".format(coordinates[i][0])),float("{:.3f}".format(coordinates[i][1])))
#       dest = (float("{:.3f}".format(coordinates[i+1][0])),float("{:.3f}".format(coordinates[i+1][1])))
#       print(f"Orig: {orig}, Dest: {dest}")
#       # route = tc.distance.shortest_path(track, orig, dest)
#       # print(f"Route: {route}")

# #  plot tracks graph and check if coords are the same
#   for node in tracks.nodes:
#     print(f"Node: {tracks[node]}")
#   for line, coordinates in line_coordinates.items():
#     print(f"Line: {line, coordinates}")
#   for line, coordinates in line_coordinates.items():
#     print(f"Line: {line, coordinates}")


'''
  for line, coordinates in line_coordinates.items():
    print(f"Line: {line, coordinates}")
    track = nx.Graph()
    for i in range(len(coordinates)-1):
      orig = ox.nearest_nodes(track, coordinates[i][0],coordinates[i][1])
      dest = ox.nearest_nodes(track, coordinates[i+1][0],coordinates[i+1][1])
      distance = ((orig[0]-dest[0])**2 + (orig[1]-dest[1])**2)**0.5
      route = nx.shortest_path(track, orig, dest)
      if line not in routes:
        routes[line] = []
      routes[line].append((route, distance))
  print(f'routes: {routes}')
'''