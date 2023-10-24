from pathlib import Path

from src.visualisation.images.osmnx import visualize_tram_stops
from src.acquisition.acquire_data import acquire
from src.acquisition.osmnx.tram_tracks import get_train_track_graph
from src.acquisition.osmnx.tram_stops import get_train_stops_gdf
import geopandas as gpd
from shapely.geometry import Point

def main():
    #   TODO: write script that make data/generated/data and data/generated/images
    #acquire(Path("./data/generated/data/"))
    visualize_tram_stops()

def generate_stops_data(): #wiem, ze nie powinno byc to w mainie, przeniose to w sr - robcio
    g: gpd.GeoDataFrame = get_train_stops_gdf()
    
    points: list = g.geometry

    with open('gsd.txt', 'w') as f:
        for point in points[:-1]:
            f.write(str(point.x) + " " + str(point.y) + "\n")
        point_coords = list(points[-1].exterior.coords)
        point_objects = [Point(coord) for coord in point_coords]
        for po in point_objects:
            f.write(str(po.x) + " " + str(po.y) + "\n")

if __name__ == '__main__':
    main()