if __name__ == '__main__':
	from swingbye.cphysics import World, Entity, vec2

	world = World()
	world.add_planet(anchor=vec2(2.0, 3.0))
	world.add_planet(maxis=5.0)
	world.add_planet(maxis=2.0)
	world.planets[1].set_parent(world.planets[0])
	world.planets[2].set_parent(world.planets[1])
	print(world)

	print('>>> appending a ship to world')
	world.add_entity(pos=vec2(100.0, 100.0))
	print(world)

	print('>>> stepping 4 times by dt=10 and printing ship position')
	world.step(10)
	print(world.entities[0].pos)
	world.step(10)
	print(world.entities[0].pos)
	world.step(10)
	print(world.entities[0].pos)
	world.step(10)
	print(world.entities[0].pos)

	print('>>> getting predictions')
	ship = Entity(pos=vec2(100.0, 100.0))
	print(world.get_predictions(ship, 0, 40, 4))

	print('>>> timing 1000 entity predictions')
	from time import time
	start = time()
	world.get_predictions(ship, 0, 40, 1000)
	end = time()
	print(f'{end-start:.6f}s')
