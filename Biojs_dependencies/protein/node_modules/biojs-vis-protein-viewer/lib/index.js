/*
 * biojs-vis-protein-viewer
 * https://github.com/yeastgenome/biojs-vis-protein-viewer
 *
 * Copyright (c) 2015 Travis Sheppard
 * Licensed under the MIT license.
 */

/**
@class biojsvisproteinviewer
 */
"use strict";
var React = require("react");
var SGDProteinViewer = require("sgd_visualization").ProteinViewer;

var BioJsProteinViewer = function (options) {
	this.el = options.el;
	this.data = options.data;
	this.locusData = options.locusData
};
    
Object.defineProperty(BioJsProteinViewer.prototype, "render", {
	writable: true,
	configurable: true,
	value: function() {
		React.render(React.createElement(SGDProteinViewer, { data: this.data, locusData: this.locusData }), this.el);
	}
});

module.exports = BioJsProteinViewer;
