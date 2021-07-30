def main():
	import pyglet
	from .pygletengine.controller import ViewController

	pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
	pyglet.options['search_local_libs'] = True

	window = ViewController(caption='Swing BYE', resizable=True)
	pyglet.clock.schedule_interval(window.update, window.frame_rate)

	pyglet.app.run()

if __name__ == '__main__':
	main()


