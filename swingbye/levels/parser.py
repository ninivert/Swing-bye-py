# temporary, remove this
import pyglet
pyglet.resource.path = ['../']
pyglet.resource.reindex()


import pyglet
import logging
from swingbye.cphysics import vec2
# from swingbye.logic.ship import Ship
# from swingbye.logic.planet import Planet
from swingbye.logic.world import World
from swingbye.logic.planet import Planet
from swingbye.pygletengine.utils import create_sprite
from swingbye.pygletengine.components.paths import PointPath, LinePath
from swingbye.pygletengine.gameobjects.entities import ShipObject, PlanetObject
from swingbye.pygletengine.globals import GameEntity

_logger = logging.getLogger(__name__)


def parse_level(level: dict, batch: pyglet.graphics.Batch, group: pyglet.graphics.OrderedGroup) -> World:
	world = World()
	queue = [(child_dict, None) for child_dict in level['world']]

	while queue:
		child_dict, parent = queue.pop()

		# Convert the position list to a vec2
		if 'pos' in child_dict:
			child_dict['pos'] = vec2(*child_dict['pos'])
		if 'anchor' in child_dict:
			child_dict['anchor'] = vec2(*child_dict['anchor'])

		_logger.debug(f'parsing {child_dict}')

		if child_dict['type'] in ['planet', 'wormhole']:
			# Try world.add_planet()
			# then trying to assign a new subclass ?
			world.add_planet(Planet(mass=69))

	return world


if __name__ == '__main__':
	import json
	import pyglet

	with open('swingbye/levels/level1.json') as file:
		level = json.load(file)

	batch = pyglet.graphics.Batch()
	group = pyglet.graphics.OrderedGroup(1)
	world = parse_level(level, batch, group)

	print(world)

	print(world.planets[0].prediction)





# planets = []
# ship = None
# queue = [(child_dict, None) for child_dict in level['world']]

# while queue:
# 	child_dict, parent = queue.pop()

# 	# Convert the position list to a numpy array
# 	if 'pos' in child_dict:
# 		child_dict['pos'] = np.array(child_dict['pos'])
# 	if 'anchor' in child_dict:
# 		child_dict['anchor'] = np.array(child_dict['anchor'])

# 	_logger.debug(f'parsing {child_dict}')

# 	if child_dict['type'] in ['planet', 'wormhole']:
# 		planetobject = PlanetObject(
# 			sprite=create_sprite(child_dict['sprite'], subpixel=True, batch=batch, group=pyglet.graphics.OrderedGroup(0, parent=group)),
# 			# TODO: colors
# 			path=PointPath(batch=batch, point_count=PLANET_PREDICTION_N),
# 			# TODO : named planets
# 			# name=child_dict['name'],
# 			parent=parent,
# 			game_entity=GameEntity.PLANET if child_dict['type'] == 'planet' else GameEntity.WORMHOLE,
# 			**child_dict['arguments']
# 		)
# 		queue += [(_child_dict, planetobject) for _child_dict in child_dict['children']]
# 		planets.append(planetobject)

# 	elif child_dict['type'] == 'ship':
# 		if ship is not None:
# 			_logger.warning(f'more than one ship in level, ignoring')
# 			_logger.debug(level)
# 			continue

# 		ship = ShipObject(
# 			sprite=create_sprite(child_dict['sprite'], anchor='center', subpixel=True, batch=batch, group=pyglet.graphics.OrderedGroup(0, parent=group)),
# 			path=LinePath(batch=batch, point_count=SHIP_PREDICTION_N),
# 			parent=parent,
# 			**child_dict['arguments']
# 		)

# 	else:
# 		_logger.warning(f'type `{child_dict["type"]}` is not recognized.')

# if ship is None:
# 	# TODO : world without ship ?
# 	_logger.warning(f'no ship found, instanciating default ship')
# 	ship = Ship()

# world = World(ship=ship, planets=planets, integrator=RK4Integrator)
# _logger.debug(f'finished parsing level, result\n`{world}`')
