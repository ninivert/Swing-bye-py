def main():
	import pyglet
	import glooey
	from .views.mainmenu import vbox  # HACK : run the pyglet stuff

	window = pyglet.window.Window()
	gui = glooey.Gui(window)
	gui.add(vbox)

	# TODO : find a way of decoupling global context, use ~ `window.run()`
	pyglet.app.run()

if __name__ == '__main__':
	main()
