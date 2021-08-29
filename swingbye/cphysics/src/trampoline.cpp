#ifndef __TRAMPOLINE_HPP__
#define __TRAMPOLINE_HPP__

#include "entity.hpp"
#include "planet.hpp"
#include <pybind11/smart_holder.h>

// we need a trampoline class to bridge polymorphism with python
// https://pybind11.readthedocs.io/en/stable/advanced/classes.html#operator-overloading
// also see about life extension
// https://github.com/pybind/pybind11/blob/smart_holder/README_smart_holder.rst

namespace py = pybind11;

class PyEntity : public Entity, public py::trampoline_self_life_support {
public:
	using Entity::Entity;

	virtual std::string str() const override {
		PYBIND11_OVERRIDE(std::string, Entity, str);
	}
};

class PyExplicitEntity : public ExplicitEntity, public py::trampoline_self_life_support {
public:
	using ExplicitEntity::ExplicitEntity;

	virtual std::string str() const override {
		PYBIND11_OVERRIDE(std::string, ExplicitEntity, str);
	}

	virtual vec2 pos_at(double time) const override {
		PYBIND11_OVERRIDE_PURE(vec2, ExplicitEntity, pos_at, time);
	}

	virtual vec2 vel_at(double time) const override {
		PYBIND11_OVERRIDE_PURE(vec2, ExplicitEntity, vel_at, time);
	}
};

class PyPlanet : public Planet, public py::trampoline_self_life_support {
public:
	using Planet::Planet;

	virtual std::string str() const override {
		PYBIND11_OVERRIDE(std::string, Planet, str);
	}

	virtual vec2 pos_at(double time) const override {
		PYBIND11_OVERRIDE_PURE(vec2, Planet, pos_at, time);
	}

	virtual vec2 vel_at(double time) const override {
		PYBIND11_OVERRIDE_PURE(vec2, Planet, vel_at, time);
	}
};

#endif
