extends Node2D

@onready var cam2D: Node2D = $"../../Camera2D"

func _process(_delta):
	position = Vector2(1488.0 * (1 - cam2D.zoom.x)/2.0, 910.2 * (1 - cam2D.zoom.y)/2.0)
