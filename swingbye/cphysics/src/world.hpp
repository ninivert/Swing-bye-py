#ifndef __WORLD_H__
#define __WORLD_H__

#include "globals.h"
#include "vec2.hpp"
#include "entity.hpp"
#include "planet.hpp"
#include "integrator.hpp"
#include <vector>
#include <string>

class World {
	double time = 0.0;

public:
	// TODO : make these private somehow
	// but I'd need to provide a way to pybind these
	// and implementing a std::vector<Planet> const& get_planets doesn't work
	// TODO : use polymorphism instead of raw-coding the planets
	// I'd need to make the Planet class polymorphic (see planet.hpp)
	// and also figure out a way of being able to expose the planet list
	// to python, and be able to `world.planets.append(...)` to it or use the stored planets.
	// That would need a way of copying polymorphically
	// This sounds like a huge pain and it's not needed (for now, or never),
	// so if someone reads this in the future "oh, this could use some polymorphism",
	// well then you're welcome to implement it yourself :P
	std::vector<Planet> planets;
	std::vector<Entity> entities;

	World() = default;

	void step(double dt) {
		for (Entity& entity : entities) {
			// TODO : un-hardcode the integrator
			Integrator::RK4(entity, *this, &World::forces_on, time, dt);
		}
		set_time(time + dt);
	}

	void set_time(double time_) {
		time = time_;
		for (Planet& planet : planets) {
			planet.set_time(time);
		}
	}
	double get_time() const { return time; }

	Planet& get_planet(unsigned int index) { return planets[index]; }
	void add_planet(double mass_, double maxis_, double ecc_, double time0_, double incl_, double parg_, vec2 const& anchor_) { planets.push_back(Planet(mass_, maxis_, ecc_, time0_, incl_, parg_, anchor_)); }
	void rm_planet(unsigned int index) { planets.erase(planets.begin() + index); }

	Entity& get_entity(unsigned int index) { return entities[index]; }
	void add_entity(vec2 const& pos_, vec2 const& vel_, double mass_) { entities.push_back(Entity(pos_, vel_, mass_)); }
	void rm_entity(unsigned int index) { entities.erase(entities.begin() + index); }

	// TODO : predictions

	static vec2 forces_on(Entity const& entity, World const& world, double time) {
		vec2 f = vec2(0, 0);

		for (Planet const& planet : world.planets) {
			vec2 r = planet.pos_at(time) - entity.pos;
			double d = r.length();
			vec2 n = r/d;
			double doff = d + GRAVITY_SINGULARITY_OFFSET;
			f += n * GRAVITY_CST * (entity.mass + planet.mass) / (doff*doff);
		}

		return f;
	}

	std::string str() const {
		std::string ret;
		ret += "Planets:\n";
		for (Planet const& planet : planets) {
			ret += "\t" + planet.str() + "\n";
		}
		ret += "Entities:\n";
		for (Entity const& entity : entities) {
			ret += "\t" + entity.str() + "\n";
		}
		return ret;
	}
};

#endif
