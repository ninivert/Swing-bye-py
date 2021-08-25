/*
Copyright (c) 2020 Chan Jer Shyan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#ifndef __VEC2_HPP__
#define __VEC2_HPP__

#include <cmath>
#include <string>

struct vec2 {
	double x, y;

	vec2() : x(0), y(0) {}
	vec2(double x, double y) : x(x), y(y) {}
	vec2(const vec2& v) : x(v.x), y(v.y) {}

	vec2& operator=(const vec2& v) {
		x = v.x;
		y = v.y;
		return *this;
	}

	vec2 operator+(vec2 const& v) {
		return vec2(x + v.x, y + v.y);
	}
	vec2 operator-(vec2 const& v) {
		return vec2(x - v.x, y - v.y);
	}

	vec2& operator+=(vec2 const& v) {
		x += v.x;
		y += v.y;
		return *this;
	}
	vec2& operator-=(vec2 const& v) {
		x -= v.x;
		y -= v.y;
		return *this;
	}

	vec2 operator+(double s) {
		return vec2(x + s, y + s);
	}
	vec2 operator-(double s) {
		return vec2(x - s, y - s);
	}
	vec2 operator*(double s) {
		return vec2(x * s, y * s);
	}
	vec2 operator/(double s) {
		return vec2(x / s, y / s);
	}


	vec2& operator+=(double s) {
		x += s;
		y += s;
		return *this;
	}
	vec2& operator-=(double s) {
		x -= s;
		y -= s;
		return *this;
	}
	vec2& operator*=(double s) {
		x *= s;
		y *= s;
		return *this;
	}
	vec2& operator/=(double s) {
		x /= s;
		y /= s;
		return *this;
	}

	void set(double x, double y) {
		this->x = x;
		this->y = y;
	}

	void rotate(double theta) {
		double c = std::cos(theta);
		double s = std::sin(theta);
		double tx = x * c - y * s;
		double ty = x * s + y * c;
		x = tx;
		y = ty;
	}

	vec2& normalize() {
		if (length() == 0) return *this;
		*this *= (1.0 / length());
		return *this;
	}

	double length() const {
		return std::sqrt(x*x + y*y);
	}
	void truncate(double length) {
		double angle = std::atan2(y, x);
		x = length * std::cos(angle);
		y = length * std::sin(angle);
	}

	vec2 ortho() const {
		return vec2(y, -x);
	}

	static double dist(vec2 const& v1, vec2 const& v2) {
		vec2 d(v1.x - v2.x, v1.y - v2.y);
		return d.length();
	}
	static double dot(vec2 const& v1, vec2 const& v2) {
		return v1.x * v2.x + v1.y * v2.y;
	}
	static double cross(vec2 const& v1, vec2 const& v2) {
		return (v1.x * v2.y) - (v1.y * v2.x);
	}

	std::string str() const {
		return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
	}
};

#endif
