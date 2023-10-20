import osmnx as ox

from constraints import LOCATION


def gather_data():
    g = ox.project_graph(ox.graph_from_place(LOCATION, custom_filter=r'["railway"~"tram"]'))

    ox.plot_graph(g, show=True, filepath="data/generated/tram_tracks.png", figsize=(64, 64), node_size=0,
                  edge_linewidth=2, edge_color="#ffffff", save=True)


def main():
    gather_data()


if __name__ == '__main__':
    main()
