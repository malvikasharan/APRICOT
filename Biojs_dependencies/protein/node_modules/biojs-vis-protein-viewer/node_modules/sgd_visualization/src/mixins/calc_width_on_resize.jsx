/** @jsx React.DOM */

/*
	Assumes that DOMWidth is in state, and that there is an internal method called _calculateWidth, which sets the width.
	This mixin simply calls that method on resize
*/

var CalcWidthOnRisize = {
	componentDidMount: function() {
		window.addEventListener('resize', this._handleResize);
	},

	_handleResize: function () {
		if (this.isMounted()) {
			this._calculateWidth();
		}
	}
};

module.exports = CalcWidthOnRisize;
