#ifndef __INTEGRATOR_HPP__
#define __INTEGRATOR_HPP__

#include "vec2.hpp"
#include "entity.hpp"

class World;

namespace Integrator {
	void Euler(Entity& entity, World const& world, vec2 (*force_func)(Entity const&, World const&, double), double time, double dt) {
		entity.pos += entity.vel * dt;
		entity.vel += (*force_func)(entity, world, time) / entity.mass * dt;
	}

	void RK4(Entity& entity, World const& world, vec2 (*force_func)(Entity const&, World const&, double), double time, double dt) {
		// Special case for the N-body problem
		vec2 f_ti = (*force_func)(entity, world, time);
		entity.pos += entity.vel * dt/2.0;
		vec2 f_th = (*force_func)(entity, world, time + dt/2.0);
		entity.pos += entity.vel * dt/2.0;
		vec2 f_tf = (*force_func)(entity, world, time);
		entity.vel += (f_ti*1.0/6.0 + f_th*4.0/6.0 + f_tf*1.0/6.0) / entity.mass * dt;
	}
}

#endif
