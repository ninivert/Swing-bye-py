import pyglet
import glooey
import swingbye.pygletengine.components.theme as theme


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
		custom_color = theme.OVERLAY_BACKGROUND


class Bin(glooey.Bin):
	custom_alignment = 'fill'


class Dialog(glooey.dialogs.Dialog):
	custom_alignment = 'center'


# THIS IS A SPECIFIC CONTAINER FOR THE MAIN MENU, ABSOLUTELY
# NOT MADE TO BE PLACED ANYWHERE ELSE, AS IT WILL BREAK
class Freeform(glooey.Widget):

	def __init__(self):
		super().__init__()
		self._children = []
		self._child_data = {}

	@property
	def children(self):
		return self._children[:]

	def add(self, widget, x=0, y=0, width=0, height=0, centered=False):
		self._attach_child(widget)
		self._child_data[widget] = self._gen_data(x, y, width, height, centered)
		self._children.append(widget)
		self._repack_and_regroup_children()

	def remove(self, widget):
		self._detach_child(widget)
		self._children.remove(widget)
		self._repack_and_regroup_children()

	def clear(self):
		with self.hold_updates():
			for child in self._children[:]:
				self.remove(child)

	def _gen_data(self, x, y, width, height, centered):
		return {
			'x': x,
			'y': y,
			'width': width,
			'height': height,
			'centered': centered
		}

	def _make_rect(self, data):
		rect = glooey.vecrec.Rect.null()
		rect.width = data['width']
		rect.height = data['height']
		if data['centered']:
			rect.left = data['x']*self.width - rect.width/2
			rect.bottom = data['y']*self.height - rect.height/2
		else:
			rect.left = data['x']*self.width
			rect.bottom = data['y']*self.height
		return rect

	def move(self, widget, dx, dy):
		assert widget in self._children, "Widget is not in this container"
		self._child_data[widget]['x'] += dx/self.width
		self._child_data[widget]['y'] += dy/self.height
		rect = self._make_rect(self._child_data[widget])
		self.do_resize_child(widget)

	def move_to(self, widget, x, y):
		assert widget in self._children, "Widget is not in this container"
		self._child_data[widget]['x'] = x/self.width
		self._child_data[widget]['y'] = y/self.height
		rect = self._make_rect(self._child_data[widget])
		self.do_resize_child(widget)

	def do_claim(self):
		top = bottom = left = right = 0

		for child in self._children:
			top = max(top, child.claimed_rect.bottom + child.claimed_height)
			bottom = min(bottom, child.claimed_rect.bottom)
			left = min(left, child.claimed_rect.left)
			right = max(right, child.claimed_rect.left + child.claimed_width)

		return right - left, top - bottom

	def do_resize_child(self, child):
		child._resize(self._make_rect(self._child_data[child]))

	def do_resize_children(self):
		for child in self._children:
			child._resize(self._make_rect(self._child_data[child]))
