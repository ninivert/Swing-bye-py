def main():
	import pyglet
	from swingbye.pygletengine.controller import ViewController

	pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
	pyglet.options['search_local_libs'] = True
	pyglet.resource.add_font('assets/fonts/Inconsolata.ttf')

	window = ViewController(caption='Swing BYE', resizable=True)
	pyglet.clock.schedule_interval(window.update, window.frame_rate)

	pyglet.app.run()

if __name__ == '__main__':
	main()
