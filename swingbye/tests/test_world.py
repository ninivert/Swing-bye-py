if __name__ == '__main__':
	from swingbye.cphysics import World, Planet, Entity, vec2

	p1 = Planet(anchor=vec2(2.0, 3.0))
	p2 = Planet(maxis=5.0)
	p2.set_parent(p1)
	p3 = Planet(maxis=2.0)
	p3.set_parent(p2)

	ship = Entity(pos=vec2(100.0, 100.0))

	print('>>> initializing empty world')
	world = World()
	print(world)

	print('>>> appending planets to world')
	world.planets.append(p1)
	world.planets.append(p2)
	world.planets.append(p3)
	print(world)

	print('>>> appending a ship to world')
	world.entities.append(ship)
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
