var schemes = require("..");
// pure mappings
var Clustal = schemes.getScheme("clustal");
console.log(Clustal);

// dynamic color management
var schemeMgr = new schemes();

var Clustal = schemeMgr.getScheme("clustal");
console.log(Clustal)
console.log(Clustal.getColor("B"))

// Add your own scheme

schemeMgr.addStaticScheme("bscheme", {B: "#bbb"})
console.log(schemeMgr.getScheme("bscheme").getColor("B"))


// Add a dynamic scheme

// add dynamic schemes (might lead to performance decrease in same applications)
var fun = function(letter,info){
  return info.pos % 2 == 0 ? "#ccc" : "#ddd";
}
schemeMgr.addDynScheme("fscheme",fun)

var scheme = schemeMgr.getScheme("dscheme")
console.log(scheme.type)

console.log(scheme.getColor("A", {pos: 1}))
console.log(scheme.getColor("A", {pos: 2}))
