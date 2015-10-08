var _ = require('underscore');
var viewType = require("backbone-viewj");
var pluginator;

/**
 * Remove an element and provide a function that inserts it into its original position
 * @param element {Element} The element to be temporarily removed
 * @return {Function} A function that inserts the element into its original position
 **/
function removeToInsertLater(element) {
  var parentNode = element.parentNode;
  var nextSibling = element.nextSibling;
  parentNode.removeChild(element);
  return function() {
    if (nextSibling) {
      parentNode.insertBefore(element, nextSibling);
    } else {
      parentNode.appendChild(element);
    }
  };
}

var removeChilds = function (node) {
    var last;
    while (last = node.lastChild) node.removeChild(last);
};

module.exports = pluginator = viewType.extend({
  renderSubviews: function() {
    // it is faster to remove the entire element and replace it
    // -> however this will lead to lost id,class and style props
    var oldEl = this.el;

    // it might be that the element is not on the DOM yet
    var elOnDom = oldEl.parentNode != undefined;
    if(elOnDom){
      var insert = removeToInsertLater(oldEl)
    }
    removeChilds(oldEl);

    var frag = document.createDocumentFragment();
    var views = this._views();
    var viewsSorted = _.sortBy(views, function(el) {
      return el.ordering;
    });
    var view, node;
    for (var i = 0; i <  viewsSorted.length; i++) {
      view = viewsSorted[i];
      view.render();
      node = view.el;
      if (node != null) {
        frag.appendChild(node);
      }
    }

    oldEl.appendChild(frag);
    if(elOnDom){
      insert();
    }
    return oldEl;
  },
  addView: function(key, view) {
    var views = this._views();
    if (view == null) {
      throw "Invalid plugin. ";
    }
    if (view.ordering == null) {
      view.ordering = key;
    }
    return views[key] = view;
  },
  removeViews: function() {
    var el, key;
    var views = this._views();
    for (key in views) {
      el = views[key];
      el.undelegateEvents();
      el.unbind();
      if (el.removeViews != null) {
        el.removeViews();
      }
      el.remove();
    }
    return this.views = {};
  },
  removeView: function(key) {
    var views = this._views();
    views[key].remove();
    return delete views[key];
  },
  getView: function(key) {
    var views = this._views();
    return views[key];
  },
  remove: function() {
    this.removeViews();
    return viewType.prototype.remove.apply(this);
  },
  _views: function() {
    if (this.views == null) {
      this.views = {};
    }
    return this.views;
  }
});
