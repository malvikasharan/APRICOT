msa-colorschemes
======================

A bundle of different biological color schemes.

[![NPM version](http://img.shields.io/npm/v/msa-colorschemes.svg)](https://www.npmjs.org/package/msa-colorschemes) 
[![Build Status](https://secure.travis-ci.org/greenify/msa-colorschemes.png?branch=master)](http://travis-ci.org/greenify/msa-colorschemes) 


```
npm install msa-colorschemes --save
```

How to use
----------

```
var schemes = require("msa-colorschemes");
// pure mappings
var Clustal = schemes.getScheme("clustal");
> {A: "orange", B: "#fff", ...} 

// dynamic color management
var schemeMgr = new schemes();

var Clustal = schemeMgr.getScheme("clustal");
> { default: "#ffffff",
    type: "static",
    map: {A: "orange", ... },
	getColor = function(letter)
  }
Clustal.getColor("B")
> "#fff"
```

### Add your own scheme

```
schemeMgr.addStaticScheme("bscheme", {B: "#bbb"})
schemeMgr.getScheme("bscheme").getColor("B")
> "#bbb"
```

### Add a dynamic scheme

```
var fun = schemeMgr.addDynScheme("fscheme", function(letter,info){
	return info.pos % 2 == 0 ? "#ccc" : "#ddd";
})

var scheme = schemeMgr.getScheme("dscheme")
scheme.type
> "dyn"

scheme.getColor("A", {pos: 1})
> "#ccc"
scheme.getColor("A", {pos: 2})
> "#ddd"

```

### What default schemes are provided?

Have a look in the source code.

*  `buried_index` (aka `buried`)
*  `cinema`
*  `clustal2`
*  `clustal`
*  `helix_propensity` (aka `helix`)
*  `hydro`
*  `lesk`
*  `mae`
*  `nucleotide`
*  `purine_pyrimidine` (aka `purine`)
*  `strand_propensity` (aka `strand`)
*  `taylor`
*  `turn_propensity` (aka `turn`)
*  `zappo`


Contributions
---------------

You have another color scheme or want to improve this package - contributions are highly welcome.

References
----------

* [Clustal][jalview]
* [Zappo][jalview]
* [Taylor][jalview]
* [Hydrophobicity][jalview]
* [Helix propensity][jalview]
* [Strand propensity][jalview]
* [Turn propensity][jalview]
* [Buried index][jalview]
* [Nucleotide][jalview]
* [Purine/Pyrimidine][jalview]

[jalview]: http://www.jalview.org/help/html/colourSchemes/
