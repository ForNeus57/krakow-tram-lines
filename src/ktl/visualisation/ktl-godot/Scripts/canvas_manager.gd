extends CanvasItem

var item_data = {}
var tram_data = {}
var arrival_data = {}
var people_data = {}

var stop_name_scene = preload("res://Scenes/stop_name.tscn")
var tram_population_scene = preload("res://Scenes/tram_population.tscn")
var connections: Array = []
var all_connections: Array = []
var stops: Dictionary = {} #po kolei: {nazwa: x, y, ilość linii)
var passengers: Dictionary = {}

static var global_delta: float = 0.0

var paused: bool = false
@onready var labelParentNode: Node = $LabelParent
@onready var tramCountParentNode: Node = $TramCountParent

@onready var drop_down_menu = $"../../OptionButton"
@onready var tram_data_rect = $"../../Tram Data"

static var hour = 7:
	get:
		return hour
	set(value):
		if value >= 24:
			hour = value - 24
		else:
			hour = value
static var minute = 20:
	get:
		return minute
	set(value):
		if value >= 60:
			minute = value - 60
			hour += 1
		else:
			minute = value
		global_delta = 0.0

func _ready():
	item_data = load_json_file("res://Data/tram_stops.json")[""]
	tram_data = load_json_file("res://Data/vehicles_full_data.json")
	arrival_data = load_json_file("res://Data/vehicles_arrival_times.json")
	people_data = load_json_file("res://Data/people.json")
	
	for tram in tram_data:
		tram["miejsca_zajęte_obecnie"] = 0
		var label = tram_population_scene.instantiate()
		label.text = '0'
		tramCountParentNode.add_child(label)
		tram["etykieta_ilości"] = label

	set_arrival_data()

	for passenger in people_data:
		passenger["in_tram"] = false
		passenger["current_tram_id"] = 0

	#generate_people_data()

	sorting_2D_array_by_first_two_elements(item_data)

	draw_all_stops()
	set_connections(arrival_data)
	
	add_items()
	
func add_items():
	for tram in tram_data:
		drop_down_menu.add_item(str(tram["id"]))

func generate_people_data():
	for passenger in people_data:
		var dot: int = 0
		print("PROGRESS: " + str(dot)+"/"+str(len(people_data)))
		for tram in arrival_data:
			var time: int = passenger["time"]
			var safefail: int = 5
			var time_found: bool = true
			while not passenger["in_tram"] and safefail > 0 and time_found:
				var cts_id : int = 0 #current tram stop id
				while arrival_data[tram][cts_id][1]*60+arrival_data[tram][cts_id][2] <= time and time_found:
					cts_id += 1
					if cts_id >= len(arrival_data[tram]):
						time_found = false
						print("OOPS")
				cts_id -= 1
				print(cts_id)
				if time_found and cts_id >= 0:
					var tram_td = tram_data[0] #tram from tram_data
					var i: int = 0
					while int(tram_td["id"]) != int(tram) and i < len(tram_data) - 1:
						tram_td = tram_data[i]
						i += 1
					#print("PROGRESS1: " + str(dot)+"/"+str(len(arrival_data)))
					if passenger["direction"] == arrival_data[tram][cts_id][3] and not passenger["in_tram"] and passenger["start_stop"].contains(arrival_data[tram][cts_id][0].substr(0, len(arrival_data[tram][cts_id][0])-3)) and passenger["line"] == str(tram_td["line"]) and tram_td["miejsca_zajęte_obecnie"] < tram_td["Miejsca ogółem"]:# and passenger["current_tram_id"] == 0:
						if(len(arrival_data[tram][cts_id]) == 4):
							arrival_data[tram][cts_id].append(1)
						else:
							arrival_data[tram][cts_id][4] += 1 #ten komponent będzie odpowiedzialny za to ile dodać, a ile odjąć na tym przystanku
						var ets_id: int = cts_id #exit tram stop id
						print("PROGRESS2: " + str(dot)+"/"+str(len(arrival_data)))
						while arrival_data[tram][ets_id][0] != passenger["end_stop"].substr(0, len(passenger["end_stop"])-3) and ets_id < len(arrival_data[tram]):
							ets_id += 1
						tram_td["miejsca_zajęte_obecnie"] += 1
						if(len(arrival_data[tram][ets_id]) == 4):
							arrival_data[tram][ets_id].append(-1)
						else:
							arrival_data[tram][ets_id][4] -= 1
						passenger["in_tram"] = true
					time += 1
					safefail -= 1
		dot += 1

func _process(delta):
	if not paused:
		global_delta += delta

func set_arrival_data():
	for data in arrival_data:
		for stop in arrival_data[data]:
			var l: int= len(stop[0])
			stop.append(int(stop[0].substr(l - 2, -1)))
			stop[0] = stop[0].substr(0, l - 3)

func get_specific_line(line_nr: int):
	'''
	var line_stops = []
	for stop in item_data:
		if line_nr == stop[0] or line_nr == 0:
			line_stops.append(stop)
	'''	
	var line_stops = {}
	var found: bool = false
	for tram1 in arrival_data:
		for tram2 in tram_data:
			if tram2["id"] == int(tram1) and tram2["line"] == line_nr and not found:
				line_stops[tram1] = arrival_data[tram1]
				found = true
	set_connections(line_stops)
	#queue_redraw()

func draw_all_stops():
	var unique_tram_stops = []
	var unique_tram_stops_names = []
	for item in item_data:
		if item[2] not in unique_tram_stops_names:
			unique_tram_stops.append(item)
			unique_tram_stops_names.append(item[2])
	stops = stops_positions_from_geographical_coordinates(unique_tram_stops)
	for i in item_data:
		stops[i[2].substr(0, len(i[2])-3)][1] += 1
	var stops_names = []
	for i in item_data:
		var name: String = i[2].substr(0, len(i[2])-3)
		if name not in stops_names:
			var label = stop_name_scene.instantiate()
			label.position = stops[name][0]/10.0 + Vector2(5.0, 5.0)
			label.text = name
			label.stop_name = name
			labelParentNode.add_child(label)
			stops_names.append(name)
		else:
			for l in labelParentNode.get_children():
				if name == l.stop_name:
					l.connection_number += 1

func set_connections(data):
	connections = []
	for tram_track in data: #arrival_data
		for i in range(len(data[tram_track])-1):
			var found: bool = false
			var name1: String = data[tram_track][i][0]#.substr(0, len(data[tram_track][i][0])-3)
			var name2: String = data[tram_track][i+1][0]#.substr(0, len(data[tram_track][i+1][0])-3)
			for con in connections:
				if (name1 == con[0] and name2 == con[1]) or (name2 == con[0] and name1 == con[1]):
					con[2] += 1
					found = true
			if not found:
				connections.append([name1, name2, 1])
	'''
	for i in range(len(data)-1):
		if data[i][0] == data[i+1][0] and data[i][1] + 1 == data[i+1][1]:
			var found: bool = false
			var name1: String = data[i][2].substr(0, len(data[i][2])-3)
			var name2: String = data[i+1][2] .substr(0, len(data[i+1][2])-3)
			for con in connections:
				if (name1 == con[0] and name2 == con[1]) or (name2 == con[0] and name1 == con[1]):
					con[2] += 1
					found = true
			if not found:
				print(name1+"| |"+name2)
				connections.append([name1, name2, 1])
	'''
	if len(all_connections) == 0:
		all_connections = connections
	else:
		for con in connections:
			for a_con in all_connections:
				if (a_con[0] == con[0] and a_con[1] == con[1]) or (a_con[0] == con[1] and a_con[1] == con[0]):
					con[2] = a_con[2]

#sortuje zwn pierwszy element, w przypadku równości, sortuje po drugim
func sorting_2D_array_by_first_two_elements(array2D: Array):
	var array2DSize = array2D.size()-1
	for j in range(array2DSize):
		for i in range(array2DSize,0+j,-1):
			if ((array2D[i][0]) < (array2D[i-1][0]) or ((array2D[i][0]) == (array2D[i-1][0]) and (array2D[i][1]) < (array2D[i-1][1]))):
				var temporaryStore = array2D[i-1]
				array2D[i-1] = array2D[i]
				array2D[i] = temporaryStore
	return array2D

#zwraca pozycję na mapie godota na bazie współrzędnych geograficznych
func stops_positions_from_geographical_coordinates(stops_arg: Array):
	var x_shift = 0.0
	var y_shift = 160.0
	var x_bound = 340.0
	var y_bound = 338.0
	var width = 14880.0
	var height = 9102.0
	
	var X: Array = []
	var Y: Array = []
	var Names: Array = []
	var new_dict = {}
	
	for uts in stops_arg:
		X.append(uts[3][0])
		Y.append(uts[3][1])
		Names.append(uts[2].substr(0, len(uts[2])-3))

	for i in range(len(stops_arg)):
		var xp = x_bound + x_shift + (width - x_bound * 2) * (X[i] - X.min()) / (X.max() - X.min())
		var yp = height - y_bound + y_shift - (height - y_bound * 2) * (Y[i] - Y.min()) / (Y.max() - Y.min())
		new_dict[Names[i]] = [Vector2(xp, yp), 0]

	return new_dict

func mix_colors(c1: Color, c2: Color, ratio: float) -> Color:

	ratio = clamp(ratio, 0, 1)
	
	var new_r = lerp(c1.r, c2.r, ratio)
	var new_g = lerp(c1.g, c2.g, ratio)
	var new_b = lerp(c1.b, c2.b, ratio)
	var new_a = lerp(c1.a, c2.a, ratio)

	var mixed_color = Color(new_r, new_g, new_b, new_a)
	return mixed_color

func _draw():
	var con_max = 0
	var stops_names: Array = []
	for con in connections:
		con_max = max(con[2], con_max)

	#connections
	for connection in connections:
		if connection[0] in stops.keys() and connection[1] in stops.keys():
			draw_line(stops[connection[0]][0]/10.0, stops[connection[1]][0]/10.0, mix_colors(Color.GREEN, Color.RED, float(connection[2])/float(con_max)), 4.0)
	
	#trams
	for connection in connections:
		for i in [0, 1]:
			if connection[i] not in stops_names and connection[i] in stops.keys():
				draw_circle(stops[connection[i]][0]/10.0, 10.0, mix_colors(Color.GREEN, Color.RED, float(connection[2])/float(con_max)))
				stops_names.append(connection[i])
	
	#stops names
	for l in labelParentNode.get_children():
		l.on_track = l.stop_name in stops_names
		
	#trams
	for tram in tram_data:
		var tram_stops: Array = arrival_data[str(tram["id"])]
		if len(tram_stops) > 0:
			var t_id: int = 0
			var on_stop: bool = false
			#var part: bool = false
			while ((hour > tram_stops[t_id][1]) or (hour == tram_stops[t_id][1] and minute >= tram_stops[t_id][2])) and t_id < len(tram_stops) - 1:
				t_id += 1
			t_id -= 1
			#part = tram_stops[t_id][1] < hour or (tram_stops[t_id][1] == hour and tram_stops[t_id][2] < minute)
			var start_stop_name: String = tram_stops[clamp(t_id, 0, len(tram_stops)-1)][0]
			var tram_direction = tram_stops[clamp(t_id, 0, len(tram_stops)-1)][3]
			if start_stop_name in stops.keys():
				var target_pos: Vector2 = stops[start_stop_name][0]
				var nt_id: int = clamp(t_id + 1, 0, len(tram_stops)-1)
				if tram_stops[nt_id][0] in stops.keys() and t_id < nt_id: #and part
					var next_stop_name: String = tram_stops[nt_id][0]
					if time_dif(hour, minute, tram_stops[t_id][1], tram_stops[t_id][2]) == 0:
						on_stop = true
					target_pos = lerp(target_pos, stops[next_stop_name][0], (global_delta/1.5 + time_dif(hour, minute, tram_stops[t_id][1], tram_stops[t_id][2]))/time_dif(tram_stops[nt_id][1], tram_stops[nt_id][2], tram_stops[t_id][1], tram_stops[t_id][2]))
				draw_rect(Rect2(target_pos.x/10.0 - 5.0, target_pos.y/10.0 - 5.0, 10.0, 10.0), Color.ROYAL_BLUE)
				tram["etykieta_ilości"].position = Vector2(target_pos.x/10.0 - 5.0, target_pos.y/10.0 - 10.0)

				'''if hour*60+minute == tram_stops[nt_id][1]*60+tram_stops[nt_id][2]:
					tram["miejsca_zajęte_obecnie"] = max(0, tram["miejsca_zajęte_obecnie"]+tram_stops[nt_id][4])
					tram["etykieta_ilości"].text = str(tram["miejsca_zajęte_obecnie"])
				'''
			#passengers
			if on_stop:
				for passenger in people_data:
					if not passenger["in_tram"] and passenger["start_stop"].contains(start_stop_name) and passenger["time"] <= 60*hour + minute and passenger["line"] == str(tram["line"]) and tram["miejsca_zajęte_obecnie"] < tram["Miejsca ogółem"] and passenger["current_tram_id"] == 0 and passenger["direction"] == tram_direction:
						tram["miejsca_zajęte_obecnie"] += 1
						tram["etykieta_ilości"].text = str(tram["miejsca_zajęte_obecnie"])
						passenger["in_tram"] = true
						passenger["current_tram_id"] = tram["id"]
					if passenger["in_tram"] and passenger["end_stop"].contains(start_stop_name) and passenger["current_tram_id"] == tram["id"]:
						tram["miejsca_zajęte_obecnie"] = max(0, tram["miejsca_zajęte_obecnie"]-1)
						tram["etykieta_ilości"].text = str(tram["miejsca_zajęte_obecnie"])
					
			if tram_stops[clamp(t_id-1, 0, len(tram_stops)-1)][0] == tram_stops[clamp(t_id+1, 0, len(tram_stops)-1)][0] or t_id == len(tram_stops)-1 or t_id == 0:
				tram["miejsca_zajęte_obecnie"] = 0
				tram["etykieta_ilości"].text = str(tram["miejsca_zajęte_obecnie"])
	
	#tram data rectangle
	if tram_data_rect.visible:
		for i in range(len(tram_data)):
			if tram_data[i]["id"] == tram_data_rect.current_tram_data["id"]:
				var tram_stops: Array = arrival_data[str(tram_data[i]["id"])]
				
				tram_data_rect.current_tram_data["miejsca_zajęte"] = tram_data[i]["miejsca_zajęte_obecnie"]
				
				var t_id: int = 0
				while ((hour > tram_stops[t_id][1]) or (hour == tram_stops[t_id][1] and minute >= tram_stops[t_id][2])) and t_id < len(tram_stops) - 1:
					t_id += 1
				t_id -= 1
				
				tram_data_rect.current_tram_data["następny_przystanek"] = tram_stops[min(t_id+1, len(tram_stops)-1)][0]
				tram_data_rect.update_label()
#			tram_data_rect.current_tram_data = {"id": tram_data[tram_index]["id"], "linia": tram_data[tram_index]["line"], "miejsca_zajęte":0, "miejsca_ogółem":tram_data[tram_index]["Miejsca ogółem"], "następny_przystanek": tram_stops[t_id][0], "cel":target}
func time_dif(h1: int, m1: int, h2: int, m2: int) -> float:
	if h1 == h2:
		return abs(m1 - m2)
	elif h1 > h2:
		return 60.0 * abs(h1 - hour) + m1 - m2
	else:
		return 60.0 * abs(h1 - hour) - m1 + m2
		
func load_json_file(file_path: String):
	if FileAccess.file_exists(file_path):
		var data_file = FileAccess.open(file_path, FileAccess.READ)
		var parsed_result = JSON.parse_string(data_file.get_as_text())
		#if parsed_result is Dictionary:
		return parsed_result
		#else:
		#	print("Error reading file")
	else:
		print("File doesn't exist")

func _on_line_edit_text_submitted(new_text):
	var line_nr = int(new_text)
	get_specific_line(line_nr)


func _on_next_minute_button_button_up():
	minute += 1
	queue_redraw()

func _on_minute_passed_timer_timeout():
	var minute_str: String = str(minute)
	var hour_str: String = str(hour)
	if minute < 10:
		minute_str = "0" + minute_str
	if hour < 10:
		hour_str = "0" + hour_str
	$"../../Godzina".text = str(hour_str) + ":" + str(minute_str)
	if not paused:
		minute += 1
		#queue_redraw()
	#$MinutePassedTimer.start()

func _on_pause_button_button_up():
	paused = not paused


func _on_text_enable_button_button_up():
	labelParentNode.visible = not labelParentNode.visible


func _on_next_tram_position_timer_timeout():
	if not paused:
		queue_redraw()

func _on_option_button_item_selected(index):
	tram_data_rect.visible = true
	for tram_index in range(len(tram_data)):
		if tram_index == index:
			var tram_stops: Array = arrival_data[str(tram_data[tram_index]["id"])]
			var target: String = tram_stops[0][0]
			var t_id: int = 0
			while ((hour > tram_stops[t_id][1]) or (hour == tram_stops[t_id][1] and minute >= tram_stops[t_id][2])) and t_id < len(tram_stops) - 1:
				t_id += 1
			t_id -= 1
			
			if tram_stops[t_id][3] == "START_END":
				var f_id = 1
				while tram_stops[f_id - 1][0] != tram_stops[f_id + 1][0]:
					f_id += 1
				target = tram_stops[f_id][0]

			tram_data_rect.current_tram_data = {"id": tram_data[tram_index]["id"], "linia": tram_data[tram_index]["line"], "miejsca_zajęte":tram_data[tram_index]["miejsca_zajęte_obecnie"], "miejsca_ogółem":tram_data[tram_index]["Miejsca ogółem"], "następny_przystanek": tram_stops[t_id][0], "cel":target}
			return
#TODO: tutaj dodać odpowiednie przypisywanie ctd i poszukać miejsc, w których należy je aktualizować
#var current_tram_data: Dictionary = {"id": 0, "linia":0, "miejsca_zajęte":0, "miejsca_ogółem":0, "następny_przystanek":"", "cel":""}:
'''
func find_shortest_path(graph_edges: Array, start_node: String, end_node: String) -> Array:

	var graph = {}
	
	# Tworzymy słownik reprezentujący graf
	for edge in connections:
		var node1 = edge[0]
		var node2 = edge[1]
		var weight = 1 #na razie niech każdy ma wagę 1
		
		if not graph.has(node1):
			graph[node1] = {}
		if not graph.has(node2):
			graph[node2] = {}
		
		graph[node1][node2] = weight
		graph[node2][node1] = weight

	# Inicjalizujemy koszty i poprzedników
	var costs = {}
	var parents = {}
	
	for node in graph.keys():
		costs[node] = 1000
		parents[node] = null

	costs[start_node] = 0
	var processed = {}

	# Algorytm Dijkstry
	var node = find_lowest_cost_node(costs, processed)
	while node:
		var cost = costs[node]
		var neighbors = graph[node]
		
		for neighbor in neighbors.items():
			var new_cost = cost + neighbor.value
			if new_cost < costs[neighbor.key]:
				costs[neighbor.key] = new_cost
				parents[neighbor.key] = node
		
		processed[node] = true
		node = find_lowest_cost_node(costs, processed)

	# Odtwarzamy ścieżkę
	var path = []
	var current_node = end_node
	while current_node != start_node:
		path.append(current_node)
		current_node = parents[current_node]

	path.append(start_node)
	path.reverse()

	return path

	# Funkcja pomocnicza do znajdowania wierzchołka z najniższym kosztem

func find_lowest_cost_node(costs, processed):
	var lowest_cost = 1000
	var lowest_cost_node = null
		
	for node in costs.items():
		if node.key < lowest_cost and not processed.has(node.value):
			lowest_cost = node.key
			lowest_cost_node = node.value
		
	return lowest_cost_node
'''
