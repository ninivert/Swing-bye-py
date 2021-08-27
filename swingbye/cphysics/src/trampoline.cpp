#ifndef __TRAMPOLINE_HPP__
#define __TRAMPOLINE_HPP__

#include "entity.hpp"
#include <pybind11/pybind11.h>

// we need a trampoline class to bridge polymorphism with python
// https://pybind11.readthedocs.io/en/stable/advanced/classes.html#operator-overloading

class PyExplicitEntity : public ExplicitEntity {
public:
	using ExplicitEntity::ExplicitEntity;

	virtual vec2 pos_at(double time) const override {
		PYBIND11_OVERRIDE_PURE(
			vec2,
			ExplicitEntity,
			pos_at,
			time
		);
	}

	virtual vec2 vel_at(double time) const override {
		PYBIND11_OVERRIDE_PURE(
			vec2,
			ExplicitEntity,
			vel_at,
			time
		);
	}
};

#endif
