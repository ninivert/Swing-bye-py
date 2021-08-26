#include "vec2.hpp"
#include "entity.hpp"
#include "planet.hpp"
#include "world.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

namespace py = pybind11;

PYBIND11_MODULE(cphysics, m) {
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
		.def_readwrite("mass", &Planet::mass)
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
		.def("__repr__", [](Planet const& p) { return p.str(); });

	py::class_<World>(m, "World")
		.def_property_readonly(
			"planets",
			[](World const& world) {
				return py::list(
					py::make_iterator(
						world.planets.begin(), world.planets.end(),
						py::return_value_policy::reference
					)
				);
			},
			py::return_value_policy::reference,
			py::doc("A list of planets references, identical in memory to get_planet(index)")
		)
		.def_property_readonly(
			"entities",
			[](World const& world) {
				return py::list(
					py::make_iterator(
						world.entities.begin(), world.entities.end(),
						py::return_value_policy::reference
					)
				);
			},
			py::return_value_policy::reference,
			py::doc("A list of entities references, identical in memory to get_entity(index)")
		)
		.def_property("time", &World::get_time, &World::set_time)
		.def("forces_on", &World::forces_on)
		.def("step", &World::step)
		.def("get_predictions", &World::get_predictions)
		.def(
			"get_planet",
			&World::get_planet,
			py::return_value_policy::reference
		)
		.def(
			"add_planet", &World::add_planet,
			py::arg("mass") = 1.0,
			py::arg("maxis") = 1.0,
			py::arg("ecc") = 0.0,
			py::arg("time0") = 0.0,
			py::arg("incl") = 0.0,
			py::arg("parg") = 0.0,
			py::arg("anchor") = vec2(0, 0)
		)
		.def("rm_planet", &World::rm_planet)
		.def(
			"get_entity",
			&World::get_entity,
			py::return_value_policy::reference
		)
		.def(
			"add_entity", &World::add_entity,
			py::arg("pos") = vec2(),
			py::arg("vel") = vec2(),
			py::arg("mass") = 1.0
		)
		.def("rm_entity", &World::rm_entity)
		.def(py::init<>())
		.def("__repr__", [](World const& w) { return w.str(); });
}