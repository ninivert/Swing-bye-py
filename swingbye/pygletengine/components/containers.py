import pyglet
import glooey


class HBox(glooey.HBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class VBox(glooey.VBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class Grid(glooey.Grid):
	custom_cell_padding = 5
	custom_alignment = 'fill'
