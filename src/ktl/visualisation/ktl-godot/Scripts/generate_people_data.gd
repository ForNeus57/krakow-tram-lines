extends Node

var item_data = {}
var tram_data = {}
var arrival_data = {}
var people_data = {}
# Called when the node enters the scene tree for the first time.
func _ready():
	
	item_data = load_json_file("res://Data/tram_stops.json")[""]
	tram_data = load_json_file("res://Data/vehicles_full_data.json")
	arrival_data = load_json_file("res://Data/vehicles_arrival_times.json")
	people_data = load_json_file("res://Data/people.json")
	
	for passenger in people_data:
		passenger["in_tram"] = false
		#passenger["current_tram_id"] = 0
		
	for tram in tram_data:
		tram["miejsca_zajęte_obecnie"] = 0
	
	for passenger in people_data:
		var time: int = passenger["time"]
		for tram in arrival_data:
			if not passenger["in_tram"]:	
				var safefail: int = 5
				while not passenger["in_tram"] and safefail > 0:
					
					var cts_id : int = 0 #current tram stop id
					while arrival_data[tram][cts_id][1]*60+arrival_data[tram][cts_id][2] < time:
						cts_id += 1
					cts_id -= 1
					print(cts_id)
					# i teraz w momencie, gdy mamy ustawienie tak, by każdy człowiek był przed swoim, dopiero przypisujemy gdzie wsiadają

					#do naprawy z warunku: start_stop_name, które o ile się nie mylę jest po prostu obecnym przystankiem
					#na tym etapie tramwaje są na zasadzie gdzie są, gdy chłop się zrespi
					#najpierw musimy znaleźć tramwaj o przypisanej linii, jadący w danym kierunku
					if passenger["direction"] == arrival_data[tram][cts_id][3] and not passenger["in_tram"] and passenger["start_stop"].contains(arrival_data[tram][cts_id][0].substr(0, len(arrival_data[tram][cts_id][0])-3)) and passenger["line"] == str(tram["line"]) and tram_data[tram]["miejsca_zajęte_obecnie"] < tram_data[tram]["Miejsca ogółem"]:# and passenger["current_tram_id"] == 0:
						#do listy wsiadek
						if(len(arrival_data[tram][cts_id] == 4)):
							arrival_data[tram][cts_id].append(1)
						else:
							arrival_data[tram][cts_id][4] += 1 #ten komponent będzie odpowiedzialny za to ile dodać, a ile odjąć na tym przystanku
						#do listy wysiadek
						var ets_id: int = cts_id #exit tram stop id
						while arrival_data[tram][ets_id][0].substr(0, len(arrival_data[tram][ets_id][0])-3) != passenger["end_stop"].substr(0, len(passenger["end_stop"])-3) and ets_id < len(arrival_data[tram]):
							ets_id += 1
						tram_data[tram]["miejsca_zajęte_obecnie"] += 1
						if(len(arrival_data[tram][ets_id] == 4)):
							arrival_data[tram][ets_id].append(-1)
						else:
							arrival_data[tram][ets_id][4] -= 1
						passenger["in_tram"] = true
					#tworzymy listę wsiadek i wysiadek
					#sprawdzamy czy przypisać mu daną linię
					#in tram = true
					#jednak nie przypisujemy do passenger["target_trams"] = [(id_tramwaju, przystanek), (id_tramwaju, przystanek)...]
					time += 1
					safefail -= 1
		
		
	'''for passenger in people_data:
				if not passenger["in_tram"] and passenger["start_stop"].contains(start_stop_name) and passenger["time"] <= 60*hour + minute and passenger["line"] == str(tram["line"]) and tram["miejsca_zajęte_obecnie"] < tram["Miejsca ogółem"] and passenger["current_tram_id"] == 0:
					+tram["miejsca_zajęte_obecnie"] += 1
					tram["etykieta_ilości"].text = str(tram["miejsca_zajęte_obecnie"])
					+passenger["in_tram"] = true
					+passenger["current_tram_id"] = tram["id"]
				if passenger["in_tram"] and passenger["end_stop"].contains(start_stop_name) and passenger["current_tram_id"] == tram["id"]:
					tram["miejsca_zajęte_obecnie"] = max(0, tram["miejsca_zajęte_obecnie"]-1)
					tram["etykieta_ilości"].text = str(tram["miejsca_zajęte_obecnie"])
	'''

func load_json_file(file_path: String):
	if FileAccess.file_exists(file_path):
		var data_file = FileAccess.open(file_path, FileAccess.READ)
		var parsed_result = JSON.parse_string(data_file.get_as_text())
		return parsed_result
	else:
		print("File doesn't exist")
