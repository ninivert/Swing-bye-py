import pyglet
import numpy as np
from .globals import WINDOW_WIDTH, WINDOW_HEIGHT
from ..physics.world import World
from ..physics.planet import Planet
from ..physics.ship import Ship
from ..physics.integrator import EulerIntegrator
from ..gameobjects.planet import PlanetObject


class DVD(pyglet.shapes.Rectangle):

	def __init__(self, x, y, width, height, colors, *args, **kwargs):
		super().__init__(x, y, width, height, *args, **kwargs)

		self.dx = 90
		self.dy = 123
		self.colors = colors
		self.color_index = 0
		self.color = self.colors[self.color_index]

	def change_color(self):
		self.color_index = (self.color_index + 1) % len(self.colors)
		self.color = self.colors[self.color_index]

	def borders(self):
		if self.x < 0:
			self.x = 0
			self.dx *= -1
			self.change_color()
		elif self.x + self.width > WINDOW_WIDTH:
			self.x = WINDOW_WIDTH - self.width
			self.dx *= -1
			self.change_color()
		if self.y < 0:
			self.y = 0
			self.dy *= -1
			self.change_color()
		elif self.y + self.height > WINDOW_HEIGHT:
			self.y = WINDOW_HEIGHT - self.height
			self.dy *= -1
			self.change_color()

	def update(self, dt):
		self.x += self.dx * dt
		self.y += self.dy * dt
		self.borders()


class LevelTransformGroup(pyglet.graphics.Group):

	def __init__(self, ctx, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ctx = ctx

	def to_world_space(self, x, y):
		return (
			(x+(self.ctx.dx*self.ctx.zoom_factor))*self.ctx.zoom_factor, 
			(y+(self.ctx.dy*self.ctx.zoom_factor))*self.ctx.zoom_factor, 
		)

	def set_state(self):
		pyglet.gl.glPushMatrix()
		pyglet.gl.glTranslatef(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 0)
		pyglet.gl.glScalef(self.ctx.zoom_factor, self.ctx.zoom_factor, 1)
		pyglet.gl.glTranslatef(self.ctx.dx/self.ctx.zoom_factor, self.ctx.dy/self.ctx.zoom_factor, 0)

	def unset_state(self):
		pyglet.gl.glPopMatrix()

class Level:

	def __init__(self, ctx):
		self.ctx = ctx
		self.current_level = 0
		self.total_levels = 10

	def load_level(self):

		world_group = LevelTransformGroup(self.ctx)

		ship = Ship()

		#        .`                                  `.             
		#       bBBBBNbh}r_                  ~rxa8NBBBBg            
		#        ^"!1L2MBBBB8L'          'imBBBBB2T<!"^`            
		#             ^BBBBBBBBK'      'GBBBBBBBB"                  
		#         .!smNBBBBN0OmU_      _XmO$NBBBBNOn!'              
		#      "eMBBNmx!~`                    `~!xENBBQS"           
		#     eBBD7_          `~"!<**<+"_`          _vDBBe          
		#      '.         _LhMBBBBBBNNBBBBMkL^         `'           
		#              ~eQBBB0mZylT77tseZKgBBBQy^                   
		#            ^DBBgX7r!!!!!!!!!!!!!!=}GNBBb!                 
		#           2BBRl!!!!!LVes=!!!!!!!!!!!=egBBS                
		#          DBBmr!!!!!!Leez=!!!!!!!!!!!!!1$BB8               
		#         lBBB1!!!!!!!!!!!!!!!!}yzL!!!!!!}NBBh              
		#         bBBB=!!!!!!!!!!!!!!!+zeet!!!!!!TNBBB              
		#         <NBB=!!!!!!!!!!!!!!!!!r+!!!!!!!tBBNl              
		#           .`"!!!!!!!!!!!!!!!!!!!!!!!!!!^`.                
		#             "!!!!!!!!!!!!!!!!!Lxt*!!!!!_                  
		#             "!!!!!!<vv1!!!!!!>eeen!!!!!_                  
		#             "!!!!!seeeex!!!!!!r*>!!!!!!_                  
		#     `'_"!!!!!!!!!+neeees!!!!!!!!!!!!!!!!!!!!"_'           
		# '"!!!!!!!!!!!!!!!!!*Li>!!!!!!!!!!!!!!!!!!!!!!!!!!!".      
		#             `.-~^""!!!!!!!!!!!!!!""^~'.`                  

		planet1_img = pyglet.resource.image('assets/sprites/planet1.png')
		planet2_img = pyglet.resource.image('assets/sprites/planet2.png')
		planet3_img = pyglet.resource.image('assets/sprites/planet3.png')
		planet4_img = pyglet.resource.image('assets/sprites/planet4.png')
		planet6_img = pyglet.resource.image('assets/sprites/planet5.png')
		planet5_img = pyglet.resource.image('assets/sprites/star1.png')
		planet1_img.anchor_x = planet1_img.width//2
		planet1_img.anchor_y = planet1_img.height//2
		planet2_img.anchor_x = planet2_img.width//2
		planet2_img.anchor_y = planet2_img.height//2
		planet3_img.anchor_x = planet3_img.width//2
		planet3_img.anchor_y = planet3_img.height//2
		planet4_img.anchor_x = planet4_img.width//2
		planet4_img.anchor_y = planet4_img.height//2
		planet5_img.anchor_x = planet5_img.width//2
		planet5_img.anchor_y = planet5_img.height//2
		planet6_img.anchor_x = planet6_img.width//2
		planet6_img.anchor_y = planet6_img.height//2


		planet1 = pyglet.sprite.Sprite(planet1_img, batch=self.ctx.batch, group=world_group)
		planet2 = pyglet.sprite.Sprite(planet2_img, batch=self.ctx.batch, group=world_group)
		planet3 = pyglet.sprite.Sprite(planet3_img, batch=self.ctx.batch, group=world_group)
		planet4 = pyglet.sprite.Sprite(planet4_img, batch=self.ctx.batch, group=world_group)
		planet5 = pyglet.sprite.Sprite(planet5_img, batch=self.ctx.batch, group=world_group)
		planet6 = pyglet.sprite.Sprite(planet6_img, batch=self.ctx.batch, group=world_group)

		sun = PlanetObject(planet5, 200, x=np.array([0, 0]), m=20)
		planets = [
			sun,
			earth := PlanetObject(planet1, 20, s=400, parent=sun),
			moon := PlanetObject(planet6, 5, s=34, parent=earth),
			PlanetObject(planet2, 5, s=8, parent=moon),
			PlanetObject(planet3, 55, s=600, parent=sun),
			PlanetObject(planet4, 32, s=800, parent=sun),
		]

		ìntegrator = EulerIntegrator()
		self.world = World(ship, planets, ìntegrator)



	def begin(self):
		
		self.ctx.gui.clear()

		self.load_level()

		# self.dvd = DVD(0, 0, 100, 40, [
		# 	(255, 20, 20),
		# 	(20, 255, 20),
		# 	(20, 20, 255),
		# 	(255, 255, 20),
		# 	(255, 20, 255)],
		# 	batch=self.ctx.batch
		# )

		self.ctx.game_loop = self.run

	def run(self, dt):
		# self.dvd.update(dt)
		self.world.t += dt * 1000
