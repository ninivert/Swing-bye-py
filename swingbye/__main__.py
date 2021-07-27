def main():
	import pyglet
	from .views.controller import ViewController


	# https://github.com/pbedn/glooey-game-hud-example
	window = ViewController(caption='Swing BYE')
	pyglet.clock.schedule_interval(window.update, window.frame_rate)

	pyglet.app.run()

if __name__ == '__main__':
	main()


