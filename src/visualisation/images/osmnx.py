from pathlib import Path

import osmnx as ox
from networkx import MultiDiGraph

from src.visualisation.images.constraints import TRAM_TRACKS_IMAGE_SIZE, LINE_COLOR
import matplotlib.pyplot as plt


def visualize_osmnx_graph(g: MultiDiGraph, path: Path) -> None:
    ox.plot_graph(g, filepath=str(path), figsize=TRAM_TRACKS_IMAGE_SIZE, node_size=0, edge_linewidth=1,
                  edge_color=LINE_COLOR, save=True)


def visualize_tram_stops() -> None:
    with open('./data/generated/data/gsd.txt', 'r') as file:
        data = [line.split() for line in file]

    data = [(float(x), float(y)) for x, y in data]
    x, y = zip(*data)

    plt.figure(figsize=(64, 64))
    plt.scatter(x, y, marker='o', color='r')
    plt.axis('off')
    plt.savefig('data/generated/images/tram_stops.png', bbox_inches='tight', pad_inches=0, dpi=300)
    # plt.show()

    '''
    TA CZĘŚĆ KODU MA ODPOWIADAĆ ZA NAKŁADANIE SIĘ OBRAZKÓW, ALE NA RAZIE NIE DZIAŁA

    tracks = Image.open('data/generated/images/tram_tracks.png')
    width, height = tracks.size
    tracks_and_stops = tracks.copy()
    draw = ImageDraw.Draw(tracks_and_stops)
    point_size = 50 
    
    adjusted_points = [(x, height - y) for x, y in data]
    for xi, yi in zip(x, y):
        x0, y0 = xi - point_size, yi - point_size
        x1, y1 = xi + point_size, yi + point_size
        draw.ellipse([x0, y0, x1, y1], fill=(0, 0, 255)) 

    tracks_and_stops.save('data/generated/images/tram_tracks_and_stops.png')

    #plt.imshow(tracks_and_stops)
    #plt.axis('off')
    #plt.show()
    '''
