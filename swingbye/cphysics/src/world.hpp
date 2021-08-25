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
	// TODO : could be more general type ExplicitEntity
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
