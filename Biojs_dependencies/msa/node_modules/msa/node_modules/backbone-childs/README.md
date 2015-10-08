backbone-childs
===============

Extends the default [Backbone view](http://backbonejs.org/#View) with support for subviews (aka child views).
It uses [backbone-viewj](https://github.com/greenify/bacbone-viewj) (backbone view with jbone) and doesn't need jQuery nor Zepto as dependecy.

Features
--------

* `ordering`: (optiona)  add this attribute to your view for custom ordering (otherwise it will order after your key)
* `key` access : views are saved in a dictionary


### renderSubviews

call this command in your render function to render all subviews.

### addView(view,key)

adds a view with `key`.
If you don't have a `ordering` attribute it will set your `key` as ordering attribute.

### getView (key)

gets the view with `key`.

### removeView (key)

removes the view with `key`.

### removeViews()

destroys all child views.

### remove()

destroys this view
