if __name__ == '__main__':
	from swingbye.cphysics import World, vec2, Planet

	print('>>> initializing empty world')
	world = World()
	print(world)

	print('>>> appending planets to world by providing constructor arguments')
	world.add_planet(anchor=vec2(2.0, 3.0))
	world.add_planet(maxis=5.0)
	world.add_planet(maxis=2.0)
	world.add_planet(anchor=vec2(-69.0, -420.0))

	p0 = world.get_planet(0)
	print(f"python address {hex(id(p0))}")

	print('>>> setting parents')
	# world.get_planet(1).set_parent(world.get_planet(0))
	# world.get_planet(2).set_parent(world.get_planet(1))
	# or
	world.planets[1].set_parent(world.planets[0])
	world.planets[2].set_parent(world.planets[1])
	print(world)

	print('>>> appending planets to world by providing existing planet')
	world.add_planet_existing(Planet(anchor=vec2(-5.0, -6.0)))
	world.add_planet_existing(Planet(ecc=0.3))
	print(world)

	print('>>> appending python subclasses of planet')

	class PyPlanet(Planet):
		def __init__(self, *arg, **kwargs):
			Planet.__init__(self, *arg, **kwargs)

		def say_hello(self):
			print(f'hello from gay little planet {self}')

	world.add_planet_existing(PyPlanet(maxis=69))
	print(world)
	# world.get_planet(len(world.planets)-1).say_hello()
	# world.planets[-1].say_hello()

	print('>>> testing memory adresses of stored and getted')
	for i, planet in enumerate(world.planets):
		print(hex(id(world.get_planet(i))), hex(id(planet)), hex(id(world.planets[i])))
		assert(id(world.get_planet(i)) == id(planet) == id(world.planets[i]))
		print('OK')

	print('>>> testing setting property on a same planet got from two different methods')
	p1_fromlist = world.planets[0]
	p1_fromget = world.get_planet(0)
	print(p1_fromlist, p1_fromget, sep='\n')
	print('setting mass of planet reference fromlist')
	p1_fromlist.mass = 10.0
	print(p1_fromlist, p1_fromget, sep='\n')
	print('setting mass of planet reference fromget')
	p1_fromget.mass = 5.0
	print(p1_fromlist, p1_fromget, sep='\n')

	print('>>> removing last planet')
	world.rm_planet(len(world.planets)-1)
	print(world)

	print('>>> listing planets')
	print(world.planets)

	print('>>> appending a ship to world')
	world.add_entity(pos=vec2(100.0, 100.0))
	print(world)

	print('>>> stepping 4 times by 0.25')
	world.step(0.25)
	world.step(0.25)
	world.step(0.25)
	world.step(0.25)
	print(world)

	print('>>> printing planet stored positions at time=1')
	print(world.planets[0].pos)
	print(world.planets[1].pos)
	print(world.planets[2].pos)

	print('>>> printing planet computed positions at time=1')
	print(world.planets[0].pos_at(1))
	print(world.planets[1].pos_at(1))
	print(world.planets[2].pos_at(1))

	print('>>> setting time to 0')
	world.time = 0

	print(world)

	print('>>> stored positions of planets')
	print(world.planets[0].pos)
	print(world.planets[1].pos)
	print(world.planets[2].pos)
