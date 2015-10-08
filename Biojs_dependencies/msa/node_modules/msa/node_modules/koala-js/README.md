# koala-js

[![NPM version](http://img.shields.io/npm/v/koala-js.svg)](https://www.npmjs.org/package/koala-js) 
[![Build Status](https://secure.travis-ci.org/greenify/koala-js.png?branch=master)](http://travis-ci.org/greenify/koala-js) 
  
<p align="center">
<img alt="Koala image" src="http://i.imgur.com/qHQSS9Om.jpg" />
</p>

A convenience collection of methods that to save unnecessary key strokes (for all the lazy coders out there). Feel free to use and improve.

## Getting Started

Install the module with: `npm install koala-js`

```javascript
var k = require('koala-js');
```

### k.d || k.defaultValue(obj, defaultValue)

Pass an alternative default value

```
var a = {};
++l.d(a.b, 1)
// returns 2
```

### k.mk || makeElement(name)

Just an alias for `document.createElement(name)`

### k.id 

Just an alias for `document.getElementById(id)`


## Support

If you have any problem or suggestion please open an issue [here](https://github.com/greenify/koala-js/issues).

## Support

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
