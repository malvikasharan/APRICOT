copy2clipboard
==============

> Copy to the clipboard without using any flash.

You can populate any content into the clipboard when the user presses "CTRL-C".

It basically attaches to the "CTRL" key events and creates a hidden, selected textarea. 
Inspired by Trello.

Install
-------

```
npm install copy2clipboard --save
```

Use
-----

```
var ClipBoard = require("./clipboard.js");
var clip = new ClipBoard();
clip.set("fancy clipboard"); // set any content
```

Test it
-------

[Click here](https://cdn.rawgit.com/greenify/copy2clipboard/master/test.html).

License
-------

MIT
