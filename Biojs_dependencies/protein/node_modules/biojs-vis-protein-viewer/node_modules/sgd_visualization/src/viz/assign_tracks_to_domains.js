"use strict";
var _ = require("underscore");

var isLeftOverlap, isRightOverlap, isInside;
var isOverlap = function (a, b) {
	isLeftOverlap = (a.start <= b.start && a.end >= b.start);
	isRightOverlap = (a.end >= b.end && a.start <= b.end);
	isInside = (a.start >= b.start && a.end <= b.end);
	return (isLeftOverlap || isRightOverlap || isInside);
}

var AssignTracksToDomains = function (domains) {
	// split by groups
	var groupedDomains = _.groupBy(domains, function (d) {
		return d.source.id;
	});

	// in each group, assign tracks
	var gDomains, trackedGDomains, groupOverlaps;
	for (var key in groupedDomains) {
		gDomains = _.sortBy(groupedDomains[key], function (d) { return d.start; });
		trackedGDomains = gDomains.map( function (d, i) {
			groupOverlaps = _.filter(gDomains, function (_d) {
				return isOverlap(d, _d);
			});
			groupOverlaps = _.sortBy(groupOverlaps, function (d) { return d.start; });
			d._track = groupOverlaps.indexOf(d);
			return d;
		});
	}

	// combine again
	var merged = [];
	merged = merged.concat.apply(merged, _.values(groupedDomains));
	merged = _.sortBy(merged, function (d) {
		return d.source.id;
	});
	return merged;
};

module.exports = AssignTracksToDomains;
