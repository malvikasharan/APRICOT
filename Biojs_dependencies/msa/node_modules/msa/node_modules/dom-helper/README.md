dom-helper
===========

A simple util lib for fast DOM operations.

### removeToInsertLater(element)

Remove an element and provide a function that inserts it into its original position
Recommended by the [Google JS speed guide](https://developers.google.com/speed/articles/javascript-dom)

@param __element__ {Element} The element to be temporarily removed
@return __callback__ {Function} A function that inserts the element into its original position

### removeAllChilds(element)

[fastest](http://jsperf.com/innerhtml-vs-removechild/15) possible way to destroy all sub nodes (aka childs)

@param __element__ {DOM Node} The element for which all childs should be removed
