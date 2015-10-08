# biojs-io-gff

[![Build Status](https://secure.travis-ci.org/greenify/biojs-io-gff.png?branch=master)](http://travis-ci.org/greenify/biojs-io-gff)
[![NPM version](https://badge-me.herokuapp.com/api/npm/biojs-io-gff.png)](http://badges.enytc.com/for/npm/biojs-io-gff) 

> A GFF (general feature format) parser

[Official Spec](https://www.sanger.ac.uk/resources/software/gff/spec.html)

```
<seqname> <source> <feature> <start> <end> <score> <strand> <frame> [attributes] [comments]
```

Short [description about the formats](https://github.com/greenify/biojs-vis-msa/wiki/Annotation-Features).

## Supported formats

* [GFF 3](http://www.sequenceontology.org/gff3.shtml)
* [Jalview feature format](http://www.jalview.org/help/html/features/featuresFormat.html)

## Getting Started
Install the module with: `npm install biojs-io-gff`

```javascript
var gff = require('biojs-io-gff');
```

## Documentation

#### `.read(file, cb)`

Callback with `parseSeqs` or Promise

```javascript
var p = gff.read("https://cdn.rawgit.com/greenify/biojs-io-gff/master/test/import.gff3");
// ..
p.then(function(seqs){
  // handle the model
}, function(err){
	console.warn(err);
});
```

#### `.parseSeqs(str)` (alias: `parse`)

**Parameter**: `GFF file` (as string)
**Type**: `String`
**Example**: `SEQ1  EMBL  atg  103  105  .  +  0`

Returns a dictionary of all sequences. Each sequences is an array of its features.

```javascript
gff.parseSeqs('SEQ1  EMBL  atg  103  105  .  +  0');
```

__Result__

```
{ "seqs":
  { "SEQ1": 
		[ { seqname: 'SEQ1',
		    source: 'EMBL',
		    feature: 'atg',
		    start: 103,
	    	end: 105,
	    	strand: '+',
	    	frame: 0,
	    	attributes: {} } ]
  },
  "config": {
	type: "gff3"
  }
}
```

#### `.parseLines(str)`

**Parameter**: `GFF file`
**Type**: `String`
**Example**: `SEQ1  EMBL  atg  103  105  .  +  0`

The 'parse' method converts a GFF into its JSON representation.

How to use this method

```javascript
gff.parseLines('SEQ1  EMBL  atg  103  105  .  +  0');
```

__Result__

```
{ "features":
	[{ seqname: 'SEQ1',
    	source: 'EMBL',
    	feature: 'atg',
    	start: 103,
    	end: 105,
    	strand: '+',
    	frame: 0,
    	attributes: {} } ],
  "config": {
	type: "gff3"
  }
}
```
#### `.exportLines(lines)`

Return the textual GFF representation for the given lines

#### `.exportSeqs(seqs)` (alias: `export`)

Return the textual GFF representation for the given seqs

#### `.parseLine(line)`

**Parameter**: `GFF line`
**Type**: `String`
**Example**: `SEQ1  EMBL  atg  103  105  .  +  0`

The 'parseLine' method converts a GFF line into its JSON representation.


```javascript
gff.parseLine('SEQ1  EMBL  atg  103  105  .  +  0');
```

## Gotchas

* undefined properties (dots) are removed (checking for undefined is native)

## Contributing

Please submit all issues and pull requests to the [greenify/biojs-io-gff](http://github.com/greenify/biojs-io-gff) repository!

## Support
If you have any problem or suggestion please open an issue [here](https://github.com/greenify/biojs-io-gff/issues).

## License 


This software is licensed under the Apache 2 license, quoted below.

Copyright (c) 2014, greenify

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
