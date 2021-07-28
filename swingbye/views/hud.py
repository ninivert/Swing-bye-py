import pyglet


class HUDgroup(pyglet.graphics.OrderedGroup):
	pass


class TimeSlider(pyglet.gui.WidgetBase):

	def __init__(self, x, y, width, height):
		pass


class wtfisthis(pyglet.gui.Slider):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def on_change(self):
		print('ok')

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		print('yep')