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


class Board(glooey.Board):
	custom_alignment = 'fill'


class Frame(glooey.Frame):
	custom_alignment = 'fill'

	class Decoration(glooey.Background):
		custom_color = '#aa1e1eff'


class Bin(glooey.Bin):
	custom_alignment = 'fill'


class Dialog(glooey.dialogs.Dialog):
	custom_alignment = 'center'
