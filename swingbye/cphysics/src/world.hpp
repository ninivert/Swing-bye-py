#ifndef __WORLD_H__
#define __WORLD_H__

#include "globals.h"
#include "vec2.hpp"
#include "entity.hpp"
#include "planet.hpp"
#include "integrator.hpp"
#include <vector>
#include <string>
#include <memory>

class World {
	double time = 0.0;

public:
	std::vector<std::shared_ptr<ExplicitEntity>> planets_ptr;
	std::vector<std::shared_ptr<Entity>> entities_ptr;

	World() = default;

	void step(double dt) {
		for (std::shared_ptr<Entity>& entity_ptr : entities_ptr) {
			// TODO : un-hardcode the integrator
			Integrator::RK4(*entity_ptr, *this, &World::forces_on, time, dt);
		}
		set_time(time + dt);
	}

	void set_time(double time_) {
		time = time_;
		for (std::shared_ptr<ExplicitEntity>& planet_ptr : planets_ptr) {
			planet_ptr->set_time(time);
		}
	}
	double get_time() const { return time; }

	std::shared_ptr<ExplicitEntity> get_planet(unsigned int index) {
		return planets_ptr[index];
	}
	void add_planet(double mass_, double maxis_, double ecc_, double time0_, double incl_, double parg_, vec2 const& anchor_) {
		planets_ptr.push_back(std::make_shared<Planet>(mass_, maxis_, ecc_, time0_, incl_, parg_, anchor_));
	}
	void add_planet_existing(std::shared_ptr<Planet> planet_ptr) {
		planets_ptr.push_back(planet_ptr);
	}
	void rm_planet(unsigned int index) {
		planets_ptr.erase(planets_ptr.begin() + index);
	}

	std::shared_ptr<Entity> get_entity(unsigned int index) {
		return entities_ptr[index];
	}
	void add_entity(vec2 const& pos_, vec2 const& vel_, double mass_) {
		entities_ptr.push_back(std::make_shared<Entity>(pos_, vel_, mass_));
	}
	void rm_entity(unsigned int index) {
		entities_ptr.erase(entities_ptr.begin() + index);
	}

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
		for (std::shared_ptr<Entity> const& entity_ptr : entities_ptr) {
			double v = entity_ptr->vel.length();
			k += 0.5 * v*v * entity_ptr->mass;
		}
		return k;
	}

	double potential_energy() const {
		double u = 0;
		for (std::shared_ptr<Entity> const& entity_ptr : entities_ptr) {
			for (std::shared_ptr<ExplicitEntity> const& planet_ptr : planets_ptr) {
				u += -GRAVITY_CST * planet_ptr->mass * entity_ptr->mass / (planet_ptr->pos - entity_ptr->pos).length();
			}
		}
		return u;
	}

	static vec2 forces_on(Entity const& entity, World const& world, double time) {
		vec2 f = vec2(0, 0);

		for (std::shared_ptr<ExplicitEntity> const& planet_ptr : world.planets_ptr) {
			vec2 r = planet_ptr->pos_at(time) - entity.pos;
			double d = r.length();
			vec2 n = r/d;
			double doff = d + GRAVITY_SINGULARITY_OFFSET;
			f += n * GRAVITY_CST * (entity.mass + planet_ptr->mass) / (doff*doff);
		}

		return f;
	}

	std::string str() const {
		std::string ret;
		ret += "ExplicitEntities:\n";
		for (std::shared_ptr<ExplicitEntity> const& planet_ptr : planets_ptr) {
			ret += "\t" + planet_ptr->str() + "\n";
		}
		ret += "Entities:\n";
		for (std::shared_ptr<Entity> const& entity_ptr : entities_ptr) {
			ret += "\t" + entity_ptr->str() + "\n";
		}
		return ret;
	}
};

#endif
