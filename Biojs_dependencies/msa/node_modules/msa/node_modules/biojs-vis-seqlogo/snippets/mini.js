var app = require("biojs-vis-seqlogo");
var counts = [];
for(var i=0;i<100;i++){
  counts.push({"A":0.25, "C":0.25, "G":0.25,"T":0.25})
}
var data = {alphabet: "aa",heightArr: counts};
inst = new app({data: data, yaxis: false,el: yourDiv, xaxis: false, height: 100});
inst.render();
