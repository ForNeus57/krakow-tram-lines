from pathlib import Path

import osmnx as ox
from networkx import MultiDiGraph

from src.visualisation.images.constraints import TRAM_TRACKS_IMAGE_SIZE, LINE_COLOR
import matplotlib.pyplot as plt

from src.acquisition.osmnx.tram_stops import get_train_stops_gdf
import geopandas as gpd
from shapely.geometry import Point
from PIL import Image, ImageDraw

def visualize_osmnx_graph(g: MultiDiGraph, path: Path) -> None:
    ox.plot_graph(g, filepath=str(path), figsize=TRAM_TRACKS_IMAGE_SIZE, node_size=0, edge_linewidth=1,
                  edge_color=LINE_COLOR, save=True)

def generate_stops_data():  # wiem, ze nie powinno byc to w mainie, przeniose to w sr - robcio
    g: gpd.GeoDataFrame = get_train_stops_gdf()

    points: list = g.geometry

    Path.mkdir(Path("./data/generated/data"), parents=True, exist_ok=True)
    Path.mkdir(Path("./data/generated/images"), parents=True, exist_ok=True)

    with open('./data/generated/data/gsd.txt', 'w') as f:
        for point in points[:-1]:
            f.write(str(point.x) + " " + str(point.y) + "\n")
        point_coords = list(points[-1].exterior.coords)
        point_objects = [Point(coord) for coord in point_coords]
        for po in point_objects:
            f.write(str(po.x) + " " + str(po.y) + "\n")

def visualize_tram_stops() -> None:
    #teraz jednocześnie generuje wspólny obraz i same przystanki
    with open('./data/generated/data/gsd.txt', 'r') as file:
        data = [line.split() for line in file]

    data = [(float(x), float(y)) for x, y in data]
    x, y = zip(*data)
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    tracks = Image.open('data/generated/images/tram_tracks.png')
    width, height = tracks.size

    stops = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    tracks_and_stops = tracks.copy()

    draw_ts = ImageDraw.Draw(tracks_and_stops)
    draw_s = ImageDraw.Draw(stops)

    point_size = 35 
    x_shift, y_shift = 0.0, 160.0
    x_bound, y_bound = 340.0, 338.0
    for xi, yi in zip(x, y):
        xp = x_bound + x_shift + (width - x_bound * 2) * (xi - x_min)/(x_max-x_min)
        yp = height - y_bound  + y_shift - (height - y_bound * 2) * (yi - y_min)/(y_max-y_min)
        draw_ts.ellipse([xp - point_size, yp - point_size, xp + point_size, yp + point_size], fill=(25, 155, 175)) 
        draw_s.ellipse([xp - point_size, yp - point_size, xp + point_size, yp + point_size], fill=(25, 155, 175)) 
    
    tracks_and_stops.save('data/generated/images/tram_tracks_and_stops.png')
    stops.save('data/generated/images/tram_stops.png')