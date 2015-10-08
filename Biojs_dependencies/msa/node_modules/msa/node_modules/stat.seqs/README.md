# stat.seqs

[![NPM version](http://img.shields.io/npm/v/stat.seqs.svg)](https://www.npmjs.org/package/stat.seqs) 
[![Build Status](https://secure.travis-ci.org/greenify/stat.seqs.png?branch=master)](http://travis-ci.org/greenify/stat.seqs) 

> A module to analyze multiple seqs (information content, frequency, ...)

## Getting Started
Install the module with: `npm install stat.seqs`

```javascript
var MSAStats = require('stat.seqs');
var seqs = ["AACG", "CACG", "AAGC", "CAAG"];
var stats = MSAStats(seqs);
```

All operations are cached, but they will be calculated again if you change the sequences.

## Operations

### Frequency

```
stats.frequency() // calculates the relative frequency of a base at a given position
> [ { A: 0.5, C: 0.5 },
  { A: 1 },
  { C: 0.5, G: 0.25, A: 0.25 },
  { C: 0.25, G: 0.75 } ]
```

### Sequence identity and consensus

```
stats.consensus() // calculates the consensus
> "AACG"

stats.identity() // identity to the consensus seq
> [ 1, 0.75, 0.5, 0.5 ]

stats.identity("AAAA") // identity to the given seq
> [ 0.5, 0.25, 0.5, 0.5 ]
```


### Background distribution

```
stats.background() // calculates the background distribution of all seqs
> { A: 0.4375, C: 0.3125, G: 0.25 }

stats.bg = {A: 0.25, C: 0.25, G: 0.25, T: 0.25} // set your own background distribution

stats.useBackground(); // use background distribution in anlysis
```

### Information content (entropy) and conservation

```
stats.ic() // calculates the information content
> [ 1, 0, 1.5, 0.81 ]

// change your alphabet
stats.setDNA(); // default
stats.setProtein();
stats.alphabetSize = 21; // your own size

// now you can scale the information content 
stats.scale(stats.ic());
> [ 0.5, 0, 0.75, 0.41 ]

stats.conservation() // needs an alphabetSize!
> [ 1, 2, 0.5, 1.19 ]
stats.scale(stats.conservation()) // scale conservation 
> [ 0.5, 1, 0.25, 0.59 ]

stats.conservResidue() // calculate conservation per residue
> [ { A: 0.5, C: 0.5 },
  { A: 2 },
  { C: 0.25, G: 0.13, A: 0.13 },
  { G: 0.89, C: 0.3 } ]

stats.conservResidue({scaled: true}) 
> [ { A: 0.25, C: 0.25 },
  { A: 1 },
  { C: 0.13, G: 0.06, A: 0.06 },
  { G: 0.45, C: 0.15 } ]
```

Scale and conservation require a set `alphabetSize` (default 4);


### Conservation with a background distribution

(work in progress)

```
stats.useBackground(); // by default from all letters

stats.ic() // calculates the information content
stats.scale(stats.ic());

stats.conservation(

stats.scale(stats.conservation())

stats.conservResidue() 

stats.conservResidue({scaled: true}) 
```

### Trivial analysis

```
stats.maxLength() 
> 4
stats.gaps() // relative percentage of gaps for a column
> [0, 0, 0, 0]
```

### Operate with the sequences

```
stats.addSeq("AAA")
stats.addSeqs(["AAA", "AAB"])
stats.resetSeqs(["AAA", "AAB"])
stats.removeSeq("AAA")
stats.removeSeq(2) // you can also use indexes
```

## Contributing

Please submit all issues and pull requests to the [greenify/stat.seqs](http://github.com/greenify/stat.seqs) repository!

## Support

If you have any problem or suggestion please open an issue [here](https://github.com/greenify/stat.seqs/issues).

## License 

The MIT License

Copyright (c) 2014, greenify

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
