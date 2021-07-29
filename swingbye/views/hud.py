import pyglet


class HUDgroup(pyglet.graphics.OrderedGroup):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.children = []

	def add(self, item):
		self.children.append(item)
		self.children[-1].parent = self

	def clear(self):
		self.children.clear()

	def update(self):
		for child in self.children:
			child.update()

	def hit(self, x, y):
		hit = False
		for child in self.children:
			hit = hit or child.hit(x, y)
		return hit

	@property
	def captured(self):
		captured = False
		for child in self.children:
			captured = captured or child.captured
		return captured

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		for child in self.children:
			if child.hit(x, y):
				child.on_mouse_scroll(x, y, scroll_x, scroll_y)

	def on_mouse_press(self, x, y, buttons, modifiers):
		for child in self.children:
			if child.hit(x, y):
				child.on_mouse_press(x, y, buttons, modifiers)

	def on_mouse_release(self, x, y, buttons, modifiers):
		for child in self.children:
			child.on_mouse_release(x, y, buttons, modifiers)

	def on_mouse_motion(self, x, y, dx, dy):
		for child in self.children:
			child.on_mouse_motion(x, y, dx, dy)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		for child in self.children:
			if child.captured:
				child.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
