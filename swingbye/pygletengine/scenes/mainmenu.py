import glooey
from pyglet.app import exit
from ..globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION
from .scene import Scene


#####################
# Main Menu Classes #
#####################


class MainMenuTitle(glooey.Label):
	custom_alignment = "center"
	custom_font_size = 60


class MainMenuContainer(glooey.VBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'

class MainMenuButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26


class MainMenuButton(glooey.Button):
	Foreground = MainMenuButtonLabel
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


##############


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def load(self):
		self.container = MainMenuContainer()
		self.container.add(MainMenuTitle('Swing BYE'), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(MainMenuButton('Start game', action=self.callback, action_params=['Level']))
		self.container.add(MainMenuButton('Select level', action=self.callback, action_params=['LevelSelectMenu']))
		self.container.add(MainMenuButton('Options', action=self.callback, action_params=['OptionsMenu']))
		self.container.add(MainMenuButton('Quit game', action=exit))

	def begin(self):
		
		self.gui.clear()

		self.load()

		self.gui.add(self.container)
	
	def draw(self):
		self.gui.batch.draw()
