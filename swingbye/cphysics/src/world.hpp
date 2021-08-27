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
	void add_planet(Planet const& planet) { planets.push_back(planet); }
	void rm_planet(unsigned int index) { planets.erase(planets.begin() + index); }

	Entity& get_entity(unsigned int index) { return entities[index]; }
	void add_entity(vec2 const& pos_, vec2 const& vel_, double mass_) { entities.push_back(Entity(pos_, vel_, mass_)); }
	void rm_entity(unsigned int index) { entities.erase(entities.begin() + index); }

	std::vector<vec2> get_predictions(Entity const& entity, double t_from, double t_to, unsigned int n) const {
		double dt = (t_to-t_from) / n;
		Entity dummy(entity);
		std::vector<vec2> predictions(n);

		for (unsigned int i=0; i < n; ++i) {
			double t = i*dt + t_from;
			Integrator::RK4(dummy, *this, &World::forces_on, t, dt);
			predictions[i] = dummy.pos;
		}

		return predictions;
	}

	double kinetic_energy() const {
		double k = 0;
		for (Entity const& entity : entities) {
			double v = entity.vel.length();
			k += 0.5 * v*v * entity.mass;
		}
		return k;
	}

	double potential_energy() const {
		double u = 0;
		for (Entity const& entity : entities) {
			for (Planet const& planet : planets) {
				u += -GRAVITY_CST * planet.mass * entity.mass / (planet.pos - entity.pos).length();
			}
		}
		return u;
	}

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
