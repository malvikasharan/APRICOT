// if you don't specify a html file, the sniper will generate a div
var menu = require("menu-builder");

var m1 = new menu({name: 'item1'});
m1.addNode("nan", function(){ console.log("nan")});
m1.addNode("pp", function(){ 
  m1.modifyNode("pp", undefined, {style: {color: "white", backgroundColor: "black"}});
  m1.render();
}, {style: {color: "red", backgroundColor: "orange"}});
m1.render();

var m2 = new menu({name: 'item2'});
m2.addNode("nan2", function(){ m2.removeNode("nan2"); m2.render(); });
m2.addNode("pp2", function(){ m2.renameNode("pp2", "pp3"); m2.render();});
m2.render();

yourDiv.appendChild(m1.el);
yourDiv.appendChild(m2.el);
