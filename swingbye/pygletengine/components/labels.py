import pyglet
import glooey
import swingbye.pygletengine.components.theme as theme


class ButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26
	custom_color = theme.TEXT
	custom_font_name = theme.FONT


class Title(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 60
	custom_color = theme.TEXT
	custom_font_name = theme.FONT


class Subtitle(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 26
	custom_color = theme.TEXT
	custom_font_name = theme.FONT


class Description(glooey.Label):
	custom_alignment = 'center'
	custom_font_size = 18
	custom_color = theme.TEXT
	custom_font_name = theme.FONT
