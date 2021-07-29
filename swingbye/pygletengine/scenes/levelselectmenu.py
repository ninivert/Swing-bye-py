import glooey
from ..globals import WINDOW_HEIGHT, TITLE_SIZE_PROPORTION
from .scene import Scene


#############################
# Level Select Menu Classes #
#############################

class LevelSelectMenuContainer(glooey.VBox):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class LevelSelectButtonsContainer(glooey.Grid):
	custom_cell_padding = 5
	custom_alignment = 'fill'


class LevelSelectMenuTitle(glooey.Label):
	custom_alignment = "center"
	custom_font_size = 60


class LevelSelectMenuButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26


class LevelSelectMenuButton(glooey.Button):
	Foreground = LevelSelectMenuButtonLabel
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



# Menu Layout

class LevelSelectMenu(Scene):

	def __init__(self, ctx, *args, **kwargs):
		super().__init__(ctx, *args, **kwargs)

	def load(self):
		self.container = LevelSelectMenuContainer()

		level_grid = LevelSelectButtonsContainer()

		for i in range(2):
			for j in range(3):
				level_grid.add(i, j, LevelSelectMenuButton(f'Level {(i+1)*(j+1)}'))
				# level_grid.add(i, j, LevelSelectMenuButton(f'Level {(i+1)*(j+1)}', action=self.ctx.views['Level'].begin, action_params=[(i+1)*(j+1)]))

		self.container.add(LevelSelectMenuTitle('Level Select'), size=int(WINDOW_HEIGHT*TITLE_SIZE_PROPORTION))
		self.container.add(level_grid)
		self.container.add(LevelSelectMenuButton('Back', action=self.ctx.views['MainMenu'].begin), size=0)

	def begin(self):
		
		self.ctx.gui.clear()

		self.load_items()

		self.ctx.gui.add(self.container)
