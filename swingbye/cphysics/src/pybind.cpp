#include "vec2.hpp"
#include "entity.hpp"
#include "planet.hpp"
#include "world.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <string>

namespace py = pybind11;

// Make these opaque so we can do something like
// >>> from cphysics import World, Planet
// >>> world = World()
// >>> world.planets.append(Planet())
// >>> world
// Planets:
// 	Planet(mass=1.000000, maxis=1.000000, ecc=0.000000, time0=0.000000, incl=0.000000, parg=0.000000, anchor=(0.000000, 0.000000))
// https://pybind11.readthedocs.io/en/stable/advanced/cast/stl.html#binding-stl-containers
PYBIND11_MAKE_OPAQUE(std::vector<Planet>);
PYBIND11_MAKE_OPAQUE(std::vector<Entity>);

PYBIND11_MODULE(cphysics, m) {
	py::bind_vector<std::vector<Planet>>(m, "ListPlanet");
	py::bind_vector<std::vector<Entity>>(m, "ListEntity");

	py::class_<vec2>(m, "vec2")
		.def_readwrite("x", &vec2::x)
		.def_readwrite("y", &vec2::y)
		.def(py::init<double, double>())
		.def(py::init<>())
		.def("length", &vec2::length)
		.def(
			"__repr__",
			[](vec2 const& v) { return v.str(); }
		);
		// TODO : bind other methods

	py::class_<Entity>(m, "Entity")
		.def_property("pos", &Entity::get_pos, &Entity::set_pos)
		.def_property("vel", &Entity::get_vel, &Entity::set_vel)
		.def_property("mass", &Entity::get_mass, &Entity::set_mass)
		.def("_set_pos", &Entity::set_pos)
		.def("_set_vel", &Entity::set_vel)
		.def("_set_mass", &Entity::set_mass)
		.def(py::init<>())
		.def(
			py::init<vec2, vec2, double>(),
			py::arg("pos") = vec2(),
			py::arg("vel") = vec2(),
			py::arg("mass") = 1.0
		);

	// py::class_<ExplicitEntity, Entity>(m, "ExplicitEntity")
	// 	.def_property_readonly("pos", &ExplicitEntity::get_pos)
	// 	.def_property_readonly("vel", &ExplicitEntity::get_vel)
	// 	.def_property_readonly("mass", &ExplicitEntity::get_mass)
	// 	.def_property("time", &ExplicitEntity::get_time, &ExplicitEntity::set_time)
	// 	.def("_set_time", &ExplicitEntity::set_time)
	// 	.def("pos_at", &ExplicitEntity::pos_at)
	// 	.def("vel_at", &ExplicitEntity::vel_at)
	// 	.def(py::init<>())
	// 	.def(py::init<double>());
		// TODO : mark as virtual

	py::class_<Planet>(m, "Planet")
		.def_property_readonly("pos", &Planet::get_pos)
		.def_property_readonly("vel", &Planet::get_vel)
		.def_property_readonly("mass", &Planet::get_mass)
		.def_readwrite("maxis", &Planet::maxis)
		.def_readwrite("ecc", &Planet::ecc)
		.def_readwrite("time0", &Planet::time0)
		.def_readwrite("incl", &Planet::incl)
		.def_readwrite("parg", &Planet::parg)
		.def_readwrite("anchor", &Planet::anchor)
		.def_property("time", &Planet::get_time, &Planet::set_time)
		.def("_set_time", &Planet::set_time)
		.def("pos_at", &Planet::pos_at)
		.def("rel_pos_at", &Planet::rel_pos_at)
		.def("vel_at", &Planet::vel_at)
		.def("set_parent", &Planet::set_parent)
		.def("rm_parent", &Planet::rm_parent)
		.def(py::init<>())
		.def(
			py::init<double, double, double, double, double, double, vec2>(),
			py::arg("mass") = 1.0,
			py::arg("maxis") = 1.0,
			py::arg("ecc") = 0.0,
			py::arg("time0") = 0.0,
			py::arg("incl") = 0.0,
			py::arg("parg") = 0.0,
			py::arg("anchor") = vec2(0, 0)
		)
		.def(
			"__repr__",
			[](Planet const& p) { return p.str(); }
		);

	py::class_<World>(m, "World")
		.def_readwrite("planets", &World::planets)
		.def_readwrite("entities", &World::entities)
		.def_property("time", &World::get_time, &World::set_time)
		.def("forces_on", &World::forces_on)
		.def("step", &World::step)
		.def(py::init<>())
		.def(
			"__repr__",
			[](World const& w) { return w.str(); }
		);
}
