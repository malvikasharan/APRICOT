biojs-io-clustal
----------------

[![Build Status](https://drone.io/github.com/greenify/biojs-io-clustal/status.png)](https://drone.io/github.com/biojs/biojs-io-clustal/latest)
[![NPM version](http://img.shields.io/npm/v/biojs-io-clustal.svg)](https://www.npmjs.org/package/biojs-io-clustal)
[![Dependencies](https://david-dm.org/greenify/biojs-io-clustal.png)](https://david-dm.org/biojs/biojs-io-clustal)
[![Code Climate](https://codeclimate.com/github/greenify/biojs-io-clustal/badges/gpa.svg)](https://codeclimate.com/github/biojs/biojs-io-clustal)
[![NPM downloads](http://img.shields.io/npm/dm/biojs-io-clustal.svg)](https://www.npmjs.org/package/biojs-io-clustal)

```
npm install biojs-io-clustal
```

Use in your browser
-------------------

[Download](https://drone.io/github.com/greenify/biojs-io-clustal/files) a compiled version for browser use.

Try out in [RequireBin](http://requirebin.com/?gist=3d961da653a8fd44e68d) or in [Codepen](http://codepen.io/greenify/pen/lnwzs).

How-to
------

#### `read(url)`

Parses an url an calls your `parse` method with the returned body.

```
Clustal.read("https://raw.githubusercontent.com/greenify/biojs-io-clustal/blob/master/test/p53.clustalo.clustal", function(err, model) {
	// model is the parsed url
});
```
If callback is undefined, `read` returns a promise.

```
Clustal.read("https://raw.githubusercontent.com/greenify/biojs-io-clustal/blob/master/test/p53.clustalo.clustal").then(function(model) {
	// model is the parsed url
}, function(err){
	console.error("err happened during downloading", err);
});
```

`function` is your async callback.

### `parse(str)`

```
var seqs = Clustal.parse(str);
```

Sequence object
---------------

```
this.seq 
this.name 
this.id 
```

License
-------

Apache 2
