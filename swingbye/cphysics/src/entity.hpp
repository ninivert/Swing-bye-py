#ifndef __ENTITY_HPP__
#define __ENTITY_HPP__

#include "vec2.hpp"
#include <string>

class Entity {
public:
	// Public in c++, but we don't expose them in python
	vec2 pos, vel;
	double mass = 1.0;

	Entity() = default;
	Entity(vec2 const& pos_, vec2 const& vel_, double mass_)
		: pos(pos_), vel(vel_), mass(mass_) {}
	Entity(double mass_) : mass(mass_) {}
	Entity(Entity const& e) : pos(e.pos), vel(e.vel), mass(e.mass) {}
	virtual ~Entity() = default;

	vec2 const& get_pos() const { return pos; }
	vec2 const& get_vel() const { return vel; }
	double get_mass() const { return mass; }
	void set_pos(vec2 const& pos_) { pos = pos_; }
	void set_vel(vec2 const& vel_) { vel = vel_; }
	void set_mass(double const& mass_) { mass = mass_; }

	virtual std::string str() const {
		return "Entity(pos=" + pos.str() + ", vel=" + vel.str() + ", mass=" + std::to_string(mass) + ")";
	}
};

class ExplicitEntity : public Entity {
protected:
	double time = 0.0;

public:
	ExplicitEntity() = default;
	ExplicitEntity(double mass_) : Entity(mass_) {}
	virtual ~ExplicitEntity() = default;

	double get_time() const { return time; }
	void set_time(double time_) {
		time = time_;
		pos = this->pos_at(time);
		vel = this->vel_at(time);
	}

	void set_pos(vec2 const& pos_) = delete;
	void set_vel(vec2 const& vel_) = delete;
	void set_mass(double const& mass_) = delete;

	virtual vec2 pos_at(double time) const = 0;
	virtual vec2 vel_at(double time) const = 0;
};

#endif
