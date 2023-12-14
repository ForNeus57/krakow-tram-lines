extends ColorRect

@onready var data_text = $Data_text

var current_tram_data: Dictionary = {"id": 0, "linia":0, "miejsca_zajęte":0, "miejsca_ogółem":0, "następny_przystanek":"", "cel":""}:
	get:
		return current_tram_data
	set(value):
		current_tram_data = value
		update_label()

func update_label():
	data_text.text = "Linia: {nr_linii}
Id: {nr_id}
Zapełnienie: {miejsca_zajęte}/{miejsca_ogółem}
Następny przystanek: 
{następny_przystanek}
Cel:
{cel}".format({"nr_linii":current_tram_data["linia"], "nr_id":current_tram_data["id"], "miejsca_zajęte":current_tram_data["miejsca_zajęte"], "miejsca_ogółem":current_tram_data["miejsca_ogółem"], "następny_przystanek":current_tram_data["następny_przystanek"], "cel":current_tram_data["cel"]})
