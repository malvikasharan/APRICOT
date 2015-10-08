biojs-io-parser
===============

A small, generic parser module.
It expects that you provide at least a method `parse` (see below for more details).


Provided methods
---------------

#### `read(url)`

Parses an url an calls your `parse` method with the returned body.

```
parser.read("http://your-url", function(err, model) {
	// model is the parsed url
});
```
If callback is undefined, `read` returns a promise.

```
parser.read("http://your-url").then(function(model) {
	// model is the parsed url
}, function(err){
	console.error("err happened during downloading", err);
});
```
 
(more to come)

Expected methods
----------------

Your parser should have the following methods:

* `parse`: Takes in an entire file as string and returns the JSON representation

Optional:

* `write`: Takes the JSON representation of a file and writes it in the custom format

If the file is line-by-line, one should create a `new` instance of the parser:

* `parseLine`: parses another line
* `result`: returns the current, resulting object of the parsing process.

How to extend
-------------

### With functions

```
var parser = function(){
  this.parse = function(data){
      return data;
  };
  Parser.mixin(this);
};
```



### With objects

```
var throughParserAlt = {
  parse: function(data) {
    return data;
  }
};
``` 


License
-------

Apache 2
