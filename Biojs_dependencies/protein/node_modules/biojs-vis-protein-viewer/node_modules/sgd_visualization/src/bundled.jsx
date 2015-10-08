/** @jsx React.DOM */
"use strict";

var React = require("react");
var SGDVisualization = require("./sgd_visualization.jsx");

// define bundled react components
var componentTypes = {
	proteinViewer: SGDVisualization.ProteinViewer
};

class BundledSGDVisualization {
	draw (options, targetNode) {
		var VizComponent = componentTypes[options.type];
		React.render(<VizComponent data={options.data} locusData={options.locusData} />, targetNode);
	}
}

window.SGDVisualization = BundledSGDVisualization;
module.exports = BundledSGDVisualization;
