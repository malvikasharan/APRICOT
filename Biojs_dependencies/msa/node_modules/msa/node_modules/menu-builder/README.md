# biojs-util-menu

[![NPM version](http://img.shields.io/npm/v/menu-builder.svg)](https://www.npmjs.org/package/menu-builder)

> A simple menu builder

## Getting Started
Install the module with: `npm install menu-builder`

```javascript
var menu = require("menu-builder");
var m1 = new menu({name: 'item1'});
m1.addNode("nan2", function(){ m2.removeNode("nan2"); m2.render(); });
m1.render();
```

You can either get DOM node by `m1.el` or pass it:

```
var m1 = new menu({name: 'item1', el: yourDiv});
```

See the [registry](http://registry.biojs.net/client/#/detail/menu-builder) for a demo.

(Don't forget to embed the css `css/menu.css`)

## Examples in applications

* [biojs-vis-msa](https://github.com/greenify/biojs-vis-msa/tree/master/src/menu/views)

## Contributing

Please submit all issues and pull requests to the [greenify/menu-builder](http://github.com/greenify/menu-builder) repository.

## Support
If you have any problem or suggestion please open an issue [here](https://github.com/greenify/menu-builder/issues).

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
