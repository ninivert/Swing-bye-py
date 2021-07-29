import glooey
from pyglet.app import exit
from .globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION
from .scenes.scene import Scene


#####################
# Main Menu Classes #
#####################

class MainMenuContainer(glooey.VBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class MainMenuButton(glooey.Button):
	custom_alignment = 'fill'

	def __init__(self, action=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.action = action

	def on_click(self, widget):
		if self.action:
			self.action()

	class Base(glooey.Background):
		custom_color = '#aa1e1e'

	class Over(glooey.Background):
		custom_color = '#cc3f3f'

	class Down(glooey.Background):
		custom_color = '#ff5d5d'


class MainMenuButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26


# Main Menu Items

class MainMenuTitle(glooey.Label):
	custom_text = "Swing BYE"
	custom_alignment = "center"
	custom_font_size = 60


class StartButtonLabel(MainMenuButtonLabel):
	custom_text = 'Start Gaming'


class StartButton(MainMenuButton):
	Foreground = StartButtonLabel


class LevelSelectButtonLabel(MainMenuButtonLabel):
	custom_text = 'Select Level'


class LevelSelectButton(MainMenuButton):
	Foreground = LevelSelectButtonLabel


class OptionsButtonLabel(MainMenuButtonLabel):
	custom_text = 'Options'


class OptionsButton(MainMenuButton):
	Foreground = OptionsButtonLabel


class QuitButtonLabel(MainMenuButtonLabel):
	custom_text = 'Quit game'


class QuitButton(MainMenuButton):
	Foreground = QuitButtonLabel


class MainMenu(Scene):

	def __init__(self, ctx, *args, **kwargs):
		super().__init__(ctx, *args, **kwargs)

	def load(self):
		self.container = MainMenuContainer()
		self.container.add(MainMenuTitle(), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(StartButton(action=self.ctx.views['Level'].begin))
		self.container.add(LevelSelectButton(action=self.ctx.views['LevelSelectMenu'].begin))
		self.container.add(OptionsButton(action=self.ctx.views['OptionsMenu'].begin))
		self.container.add(QuitButton(action=exit))

	def begin(self):
		
		self.ctx.gui.clear()

		self.load()

		self.ctx.gui.add(self.container)
