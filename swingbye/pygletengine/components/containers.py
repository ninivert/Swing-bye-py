import pyglet
import glooey
import numpy as np
import swingbye.pygletengine.components.theme as theme
from swingbye.pygletengine.components.animation import Keyframe, Animation
from swingbye.pygletengine.utils import lerp
from swingbye.pygletengine.globals import WINDOW_WIDTH, WINDOW_HEIGHT


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
	custom_box_layer = 2

	class Decoration(glooey.Background):
		custom_color = theme.OVERLAY_BACKGROUND


class Bin(glooey.Bin):
	custom_alignment = 'fill'


class Dialog(glooey.dialogs.Dialog):
	custom_alignment = 'center'


class Image(glooey.Image):
	custom_alignment = 'fill'


class Arc(glooey.Widget):
	custom_a = 360
	custom_b = 250

	def __init__(self, a=None, b=None):
		super().__init__()
		self._children = []
		self.a = a or self.custom_a
		self.b = b or self.custom_b

		self.animation = None
		self.explosion_radius = 1

	def get_children(self):
		# Return a copy of the list so the caller can't mess up our internal 
		# state by adding or removing things.
		return self._children[:]

	def get_radius(self):
		return self._radius

	def set_radius(self, radius):
		self._radius = radius
		self._repack()

	def add(self, widget):
		self.insert(widget, len(self._children))

	def insert(self, widget, index):
		self._attach_child(widget)
		self._children.insert(index, widget)
		self._repack_and_regroup_children()

	def replace(self, old_widget, new_widget):
		i = self._children.index(old_widget)
		with self.hold_updates():
			self.remove(old_widget)
			self.insert(new_widget, i)

	def remove(self, widget):
		self._detach_child(widget)
		self._children.remove(widget)
		self._repack_and_regroup_children()

	def clear(self):
		with self.hold_updates():
			for child in self._children[:]:
				self.remove(child)

	def do_claim(self):
		# Fake do_claim to be able to have widgets go offscreen
		return 0, 0

	def do_resize_children(self):
		for child, offset in self._yield_offsets():
			rect = child.claimed_rect.copy()
			rect.center = lerp(self.rect.center_left, self.rect.center, 0.5) + offset
			child._resize(rect)

	def update(self, dt):
		if self.animation is not None:
			if self.animation.done:
				pyglet.clock.unschedule(self.update)
			else:
				self.explosion_radius = self.animation.get_next_value(dt)
				self.do_resize_children()
		else:
			pyglet.clock.unschedule(self.update)

	def explode(self, explosion_radius, offset, duration):
		self.explosion_radius = 1
		self.animation = Animation(
			keyframes=[
				Keyframe(1, explosion_radius, duration, lambda a, b, t: a + ((b-a)*(1 - pow(1 - t, 3))))
			],
			repeat=False
		)
		pyglet.clock.schedule_interval(self.update, 1/60)

	def _yield_offsets(self):
		N = len(self._children) - 1
		for i, child in enumerate(self._children):
			offset = glooey.vecrec.Vector(np.sin(np.pi * (i/N)) * self.a, np.cos(np.pi * (i/N)) * self.b) * self.explosion_radius
			yield child, offset


# THIS IS A SPECIFIC CONTAINER FOR THE MAIN MENU, ABSOLUTELY
# NOT MADE TO BE PLACED ANYWHERE ELSE, AS IT WILL BREAK
class Freeform(glooey.Widget):

	def __init__(self):
		super().__init__()
		self._children = []
		self._child_data = {}
		self.old_width = WINDOW_WIDTH
		self.old_height = WINDOW_HEIGHT

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
			'modified_width': width,
			'height': height,
			'modified_height': height,
			'centered': centered
		}

	def _make_rect(self, child):
		rect = glooey.vecrec.Rect.null()
		rect.width = max(self._child_data[child]['width'], child.claimed_width)
		rect.height = max(self._child_data[child]['height'], child.claimed_height)
		if self._child_data[child]['centered']:
			rect.left = self._child_data[child]['x']*self.width - rect.width/2
			rect.bottom = self._child_data[child]['y']*self.height - rect.height/2
		else:
			rect.left = self._child_data[child]['x']*self.width
			rect.bottom = self._child_data[child]['y']*self.height
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

	def do_resize(self):
		factor_x = self.window.width / self.old_width
		factor_y = self.window.height / self.old_height
		for child in self._children:
			self._child_data[child]['width'] *= factor_x
			self._child_data[child]['height'] *= factor_y
		self.old_width = self.window.width
		self.old_height = self.window.height
		self.do_resize_children()

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
			child._resize(self._make_rect(child))
