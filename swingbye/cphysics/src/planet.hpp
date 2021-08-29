#ifndef __PLANET_HPP__
#define __PLANET_HPP__

#include "vec2.hpp"
#include "entity.hpp"
#include "globals.h"
#include <cmath>
#include <iostream>
#include <memory>

class Planet : public ExplicitEntity {
private:
	std::shared_ptr<Planet> parent = nullptr;

public:
	double maxis = 1.0;
	double ecc = 0.0;
	double time0 = 0.0;
	double incl = 0.0;
	double parg = 0.0;
	vec2 anchor = vec2();

	Planet() = default;
	Planet(double mass_, double maxis_, double ecc_, double time0_, double incl_, double parg_, vec2 anchor_)
		: ExplicitEntity(mass_), maxis(maxis_), ecc(ecc_), time0(time0_), incl(incl_), parg(parg_), anchor(anchor_) {}
	virtual ~Planet() {}

	void set_parent(std::shared_ptr<Planet> new_parent) { parent = new_parent; }
	void rm_parent() { parent.reset(); }

	virtual vec2 pos_at(double time) const override {
		vec2 ret = vec2(0, 0);
		const Planet* daddy = this;

		while (daddy != nullptr) {
			ret += daddy->rel_pos_at(time);
			if (daddy->parent == nullptr) {
				ret += daddy->anchor;
			}
			daddy = daddy->parent.get();
		}

		return ret;
	}

	vec2 rel_pos_at(double time) const {
		vec2 ret = vec2(0, 0);

		if (parent == nullptr) {
			return ret;
		}

		double mu = GRAVITY_CST*(mass + parent->mass);
		double costheta = 0, sintheta = 0, r = 0;

		if (0 <= ecc && ecc < 1) {
			double T = std::sqrt(4 * M_PI*M_PI * maxis*maxis*maxis / mu);
			double tau = std::fmod(time - time0, T);
			double n = 2*M_PI/T;
			double M = n*tau;
			double E = M;
			double dE = EPSILON_EULER + 1;
			unsigned int i = 0;

			// Solve M = E - e*sin(E)
			while (std::abs(dE) > EPSILON_EULER && i < MAX_ITER_EULER) {
				dE = (M - E + ecc*std::sin(E)) / (1 - ecc * std::cos(E));
				E += dE;
				i += 1;
			}
			if (i >= MAX_ITER_EULER) {
				std::cerr << "Euler equation solving did not escape" << std::endl;
			}

			costheta = (std::cos(E) - ecc) / (1 - ecc*std::cos(E));
			sintheta = (std::sqrt(1 - ecc*ecc) * std::sin(E)) / (1 - ecc*std::cos(E));
			r = maxis * (1 - ecc*std::cos(E));
		}

		else if (1 < ecc) {
			double tau = time - time0;
			double n = std::sqrt(-mu/(maxis*maxis*maxis));
			double M = n*tau;
			double H = M;
			double dH = EPSILON_EULER + 1;
			unsigned int i = 0;

			// Solve M = e*sinh(H) - H
			while (std::abs(dH) > EPSILON_EULER && i < MAX_ITER_EULER) {
				dH = (M - ecc*std::sinh(H) + H) / (ecc*std::cosh(H) - 1);
				H += dH;
				i += 1;
			}
			if (i >= MAX_ITER_EULER) {
				std::cerr << "Euler equation solving did not escape" << std::endl;
			}

			costheta = (ecc - std::cosh(H)) / (ecc*std::cosh(H) - 1);
			sintheta = std::copysign(1, H)*std::sin(std::acos(costheta));
			r = maxis * (1 - ecc*std::cosh(H));
		}

		ret.x = r*costheta;
		ret.y = r*sintheta;

		// Argument of periaxis
		double x = ret.x;
		double y = ret.y;
		ret.x = x*std::cos(parg) - y*std::sin(parg);
		ret.y = x*std::sin(parg) + y*std::cos(parg);

		// Inclination
		ret.x *= std::cos(incl);

		return ret;
	}

	virtual vec2 vel_at(double time) const override {
		double dt = 0.16666;
		return (pos_at(time+dt/2.0) - pos_at(time-dt/2.0)) / dt;
	}

	virtual std::string str() const override {
		return "Planet(mass=" + std::to_string(mass) + ", maxis=" + std::to_string(maxis) + ", ecc=" + std::to_string(ecc) + ", time0=" + std::to_string(time0) + ", incl=" + std::to_string(incl) + ", parg=" + std::to_string(parg) + ", anchor=" + anchor.str() + ")";
	}
};

#endif
