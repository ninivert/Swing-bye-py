#include <pybind11/smart_holder.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

#include "vec2.hpp"
#include "entity.hpp"
#include "planet.hpp"
#include "world.hpp"
#include "trampoline.cpp"

namespace py = pybind11;

PYBIND11_SMART_HOLDER_TYPE_CASTERS(Entity)
PYBIND11_SMART_HOLDER_TYPE_CASTERS(ExplicitEntity)
PYBIND11_SMART_HOLDER_TYPE_CASTERS(Planet)

PYBIND11_MODULE(cphysics, m) {
	py::class_<vec2>(m, "vec2")
		.def_readwrite("x", &vec2::x)
		.def_readwrite("y", &vec2::y)
		.def(py::init<double, double>(), py::arg("x") = 0.0, py::arg("y") = 0.0)
		.def(py::init<vec2>())
		.def(py::init<>())
		.def(py::self + py::self)
		.def(py::self - py::self)
		.def(- py::self)
		.def(py::self += py::self)
		.def(py::self -= py::self)
		.def(py::self + double())
		.def(py::self - double())
		.def(py::self * double())
		.def(py::self / double())
		.def(double() + py::self)
		.def(double() - py::self)
		.def(double() * py::self)
		.def(double() / py::self)
		.def(py::self += double())
		.def(py::self -= double())
		.def(py::self *= double())
		.def(py::self /= double())
		.def("length", &vec2::length)
		.def("set", &vec2::set)
		.def("rotate", &vec2::rotate)
		.def("normalize", &vec2::normalize)
		.def("ortho", &vec2::ortho)
		.def("copy", &vec2::copy)
		.def_static("dist", &vec2::dist)
		.def_static("dot", &vec2::dot)
		.def_static("cross", &vec2::cross)
		.def("__getitem__", [](vec2 const& v, unsigned int index) {
			if (index == 0) return v.x;
			if (index == 1) return v.y;
			throw std::out_of_range("out of bounds index `" + std::to_string(index) + "` on vec2 instance");
		})
		.def("__repr__", &vec2::str);

	py::classh<Entity, PyEntity>(m, "Entity")
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
		)
		.def("__repr__", &Entity::str);

	py::classh<ExplicitEntity, PyExplicitEntity, Entity>(m, "ExplicitEntity")
		.def(py::init<>())
		.def(py::init<double>())
		.def_property_readonly("pos", &ExplicitEntity::get_pos)
		.def_property_readonly("vel", &ExplicitEntity::get_vel)
		.def_property_readonly("mass", &ExplicitEntity::get_mass)
		.def_property("time", &ExplicitEntity::get_time, &ExplicitEntity::set_time)
		.def("_get_time", &ExplicitEntity::get_time)  // used for python property override
		.def("_set_time", &ExplicitEntity::set_time)  // used for python property override
		.def("pos_at", &ExplicitEntity::pos_at)
		.def("vel_at", &ExplicitEntity::vel_at);

	py::classh<Planet, PyPlanet, ExplicitEntity, Entity>(m, "Planet")
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
		.def("_get_time", &Planet::get_time)  // used for python property override
		.def("_set_time", &Planet::set_time)  // used for python property override
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
		.def("__repr__", &Planet::str);

	py::class_<World>(m, "World")
		.def_property_readonly(
			"planets",
			[](World const& world) {
				return py::list(
					py::make_iterator(
						world.planets_ptr.begin(), world.planets_ptr.end()
					)
				);
			},
			py::doc("A list of planets references, identical in memory to get_planet(index)")
		)
		.def_property_readonly(
			"entities",
			[](World const& world) {
				return py::list(
					py::make_iterator(
						world.entities_ptr.begin(), world.entities_ptr.end()
					)
				);
			},
			py::doc("A list of entities references, identical in memory to get_entity(index)")
		)
		.def_property("time", &World::get_time, &World::set_time)
		.def("_get_time", &World::get_time)  // used for python property override
		.def("_set_time", &World::set_time)  // used for python property override
		.def("forces_on", &World::forces_on)
		.def("step", &World::step)
		.def("kinetic_energy", &World::kinetic_energy)
		.def("potential_energy", &World::potential_energy)
		.def("get_predictions", &World::get_predictions)
		.def(
			"get_planet",
			&World::get_planet
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
		.def("add_planet_existing", &World::add_planet_existing)
		.def("rm_planet", &World::rm_planet)
		.def(
			"get_entity",
			&World::get_entity
		)
		.def(
			"add_entity", &World::add_entity,
			py::arg("pos") = vec2(),
			py::arg("vel") = vec2(),
			py::arg("mass") = 1.0
		)
		.def("add_entity_existing", &World::add_entity_existing)
		.def("rm_entity", &World::rm_entity)
		.def(py::init<>())
		.def("__repr__", &World::str);
}
