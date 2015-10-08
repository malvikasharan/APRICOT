"use strict";
var d3 = require("d3");

var HEIGHT = 17;
var POINT_WIDTH = 10;

// generates an SVG path string to draw 
var generateTrapezoidPath = function (width, orientation) {
	orientation = orientation || "right"; // points to the right, can also be left

	var startX = 0;
	var endX = width;
	var points;
	if (orientation === "right") {
		points = [
			{ x: startX, y: 0 },
			{ x: endX - POINT_WIDTH, y: 0 },
			{ x: endX, y: HEIGHT / 2 },
			{ x: endX - POINT_WIDTH, y: HEIGHT },
			{ x: startX, y: HEIGHT },
			{ x: startX, y: 0 }
		];
	} else {
		points = [
			{ x: startX + POINT_WIDTH, y: 0 },
			{ x: endX, y: 0 },
			{ x: endX, y: HEIGHT },
			{ x: startX + POINT_WIDTH, y: HEIGHT },
			{ x: startX, y: HEIGHT / 2 }
		];
	}

	var areaFn = d3.svg.line()
		.x(function (d) { return d.x; })
		.y(function (d) { return d.y; });

	return areaFn(points) + "Z";
};

module.exports = generateTrapezoidPath;
