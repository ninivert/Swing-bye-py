import glooey
import pyglet
from .globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION


########################
# Options Menu Classes #
########################

class OptionsMenuContainer(glooey.VBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class OptionsMenuTitle(glooey.Label):
	custom_alignment = "center"
	custom_font_size = 60


class OptionsMenuButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26


class OptionsMenuButton(glooey.Button):
	Foreground = OptionsMenuButtonLabel
	custom_alignment = 'fill'

	def __init__(self, *args, action=None, action_params=[], **kwargs):
		super().__init__(*args, **kwargs)
		self.action = action
		self.action_params = action_params

	def on_click(self, widget):
		if self.action:
			self.action(*self.action_params)

	class Base(glooey.Background):
		custom_color = '#aa1e1e'

	class Over(glooey.Background):
		custom_color = '#cc3f3f'

	class Down(glooey.Background):
		custom_color = '#ff5d5d'


class OptionsMenuCycle(glooey.Button):
	Foreground = OptionsMenuButtonLabel
	custom_alignment = 'fill'

	def __init__(self, states, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.states = states
		self.state_index = 0
		self.total_states = len(states)
		self.foreground.text = self.states[self.state_index]

	def on_click(self, widget):
		self.state_index = (self.state_index + 1) % self.total_states
		self.foreground.text = self.states[self.state_index]
	
	class Base(glooey.Background):
		custom_color = '#aa1e1eff'

	class Over(glooey.Background):
		custom_color = '#cc3f3fdd'

	class Down(glooey.Background):
		custom_color = '#ff5d5daa'



# Menu Layout

class OptionsMenu:

	def __init__(self, ctx):
		self.ctx = ctx
		self.loaded = False

	def load_items(self):
		self.container = OptionsMenuContainer()

		self.container.add(OptionsMenuTitle('Options'), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(OptionsMenuButton('Option Button 1'))
		self.container.add(OptionsMenuButton('Option Button 2'))
		self.container.add(OptionsMenuCycle(['Option cycle 1', 'Option cycle 2', 'Option cycle 3']))
		self.container.add(OptionsMenuCycle(['Option ON', 'Option OFF']))
		self.container.add(OptionsMenuButton('Back', action=self.ctx.views['MainMenu'].begin), size=0)

		self.loaded = True

	def unload_items(self):
		self.loaded = False
		self.container = None

	def begin(self):
		
		self.ctx.gui.clear()

		if not self.loaded:
			self.load_items()

		self.ctx.gui.add(self.container)
