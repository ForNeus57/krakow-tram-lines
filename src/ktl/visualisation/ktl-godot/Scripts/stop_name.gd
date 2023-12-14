extends Label

var stop_name: String = "stop_name"
var connection_number: int = 0
var on_track: bool = true

func _ready():
	position -= Vector2(0.0, size.y/2.0)
	#add_theme_font_size_override("tfso", 444)
	#set_size(Vector2(400, 400))
	#scale.x *= 10 - scale działa
	#scale.y *= 10
