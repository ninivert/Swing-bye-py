#ifndef ENTITY_H
#define ENTITY_H

#include "vec2.h"

namespace entity {
	struct Entity {
		vec2d pos;
		vec2d vel;
		double mass;

		Entity() = default;
		Entity(vec2d const& pos_, vec2d const& vel_, double mass_)
			: pos(pos_), vel(vel_), mass(mass_) {}
	};

	struct ExplicitEntity : public Entity {
		// TODO : dirty_pos, dirty_vel, time
		virtual vec2d pos_at(double time);
		virtual vec2d vel_at(double time);
	};
}

#endif
