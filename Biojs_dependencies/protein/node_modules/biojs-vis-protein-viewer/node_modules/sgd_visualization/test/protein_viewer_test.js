var assert = require("assert");
var React = require("react");
// jsx
require("node-jsx").install({ harmony: true });

var ProteinViewer = require("../src/sgd_visualization.jsx").ProteinViewer;

describe("ProteinViewer", function(){
	it("should render to a viz with classes 'sgd-viz' and 'protein-viewer'", function(){
		var _data = [
			{
				start: 1,
				end: 400,
				domain: {
					name: "PF0022",
				},
				source: {
					name: "Pfam",
					href: null,
					id: 1
				}
			},
			{
				start: 145,
				end: 340,
				domain: {
					name: "PF0023",
				},
				source: {
					name: "Pfam",
					href: null,
					id: 1
				}
			},
			{
				start: 245,
				end: 540,
				domain: {
					name: "Some23",
				},
				source: {
					name: "Panther",
					href: null,
					id: 1
				}
			}
		];
		var _locusData = {
			start: 0,
			end: 650,
			name: "Foo",
			href: "http://google.com"
		};

		var markup = React.renderToStaticMarkup(React.createElement(ProteinViewer, {
			data: _data,
			locusData: _locusData
		}));
		assert.equal(markup.match('class="sgd-viz protein-viewer') !== null, true);
		assert.equal(markup.match(/<div/).index, 0);
	});
});
