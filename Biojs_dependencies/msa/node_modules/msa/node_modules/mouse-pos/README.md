mouse-pos
==========

A super simple cross-browser library to get the correct coordinates of your mouse event.
Just pass the method the event obj and it will return the distance you need (as array).

```
npm install mouse-pos
```

use it like this

```
var mouse = require("mouse-pos");
var el = document.getElementById("outside");
el.addEventListener("click", function(e){
console.log("rel coords", mouse.getRel(e)); // e.g. [5,5]
console.log("abs coords", mouse.getAbs(e)); // e.g. [205,205]
});
```

#### rel(e) - relative to the target

`[x,y]`

#### abs(e) - absolute to the screen

`[x,y]`

#### wheelDelta(e)

`float` of pixels the mouse wheel moved. Could be negative.


Enjoy!
