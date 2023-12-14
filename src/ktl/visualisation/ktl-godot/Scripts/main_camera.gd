extends Camera2D

@export var min_zoom = 1.0
@export var max_zoom = 2.0
@export var zoom_factor = 1.0
@export var zoom_duration = 50

@export var shift_duration = 50

var last_mouse_pos: Vector2
var last_pos: Vector2

@onready var canvas_manager: Node2D = $"../CanvasLayer/CanvasZoomShiftManager/CanvasManager"
@onready var label_parent: Node = $"../CanvasLayer/CanvasZoomShiftManager/CanvasManager/LabelParent"
@onready var tram_count_parent: Node = $"../CanvasLayer/CanvasZoomShiftManager/CanvasManager/TramCountParent"

func _process(delta):
	if Input.is_action_just_pressed("zoom_in"):
		zoom_factor += 0.01
	elif Input.is_action_just_pressed("zoom_out"):
		zoom_factor -= 0.01
	else:
		zoom_factor = 1

	if Input.is_action_just_pressed("shifting_camera"):
		last_mouse_pos = get_viewport().get_mouse_position()

	if Input.is_action_pressed("shifting_camera"):
		last_pos = position
		canvas_manager.position = lerp(canvas_manager.position, canvas_manager.position - last_mouse_pos + get_viewport().get_mouse_position(), shift_duration * delta/zoom.x)
		canvas_manager.position = Vector2(clamp(canvas_manager.position.x, -744.0/zoom.x, 1488.0 * (1.0 - 1.0/(2*zoom.x))), clamp(canvas_manager.position.y, -455.0/zoom.y, 910.2 * (1.0 - 1.0/(2*zoom.y))))
		last_mouse_pos = get_viewport().get_mouse_position()

	zoom.x = clamp(lerp(zoom.x, zoom.x * zoom_factor, zoom_duration * delta), min_zoom, max_zoom)
	zoom.y = clamp(lerp(zoom.y, zoom.y * zoom_factor, zoom_duration * delta), min_zoom, max_zoom)
	canvas_manager.scale = Vector2(zoom.x, zoom.y)
	for l in label_parent.get_children():
		l.visible = l.on_track and (l.connection_number > 3 or (l.connection_number > 2 and zoom.x > 1.5) or zoom.x > 1.9)
		l.scale = Vector2(0.75/zoom.x, 0.75/zoom.y)
		#set_custom_font(load("res://ścieżka/do/twojej/czcionki.ttf"), 12)
	for l in tram_count_parent.get_children():
		l.scale = Vector2(0.75/zoom.x, 0.75/zoom.y)
