var schemes = require("./schemeclass");
var StaticSchemeClass = schemes.stat;
var DynSchemeClass = schemes.dyn;

var Buried = require("./buried");
var Cinema = require("./cinema");
var Clustal = require("./clustal");
var Clustal2 = require("./clustal2");
var Helix = require("./helix");
var Hydro = require("./hydrophobicity");
var Lesk = require("./lesk");
var Mae = require("./mae");
var Nucleotide = require("./nucleotide");
var Purine = require("./purine");
var Strand = require("./strand");
var Taylor = require("./taylor");
var Turn = require("./turn");
var Zappo = require("./zappo");

var staticSchemes = {
  buried: Buried,
  buried_index: Buried,
  cinema: Cinema,
  clustal2: Clustal2,
  clustal: Clustal,
  helix: Helix,
  helix_propensity: Helix,
  hydro: Hydro,
  lesk: Lesk,
  mae: Mae,
  nucleotide: Nucleotide,
  purine: Purine,
  purine_pyrimidine: Purine,
  strand: Strand,
  strand_propensity: Strand,
  taylor: Taylor,
  turn: Turn,
  turn_propensity: Turn,
  zappo: Zappo
};

var pid = require("./pid_colors.js");

var dynSchemes = {
  pid: pid
};

module.exports = Colors = function(opt){
  this.maps = clone(staticSchemes);  
  this.dyn = clone(dynSchemes);
  this.opt = opt;
}
Colors.getScheme = function(scheme){
  return staticSchemes[scheme];
}
Colors.prototype.getScheme = function(scheme) {
  var color = this.maps[scheme];
  if (color === undefined) {
    color = {};
    if(this.dyn[scheme] != undefined){
      return new DynSchemeClass(this.dyn[scheme],this.opt);
    }
  }
  return new StaticSchemeClass(color);
};

Colors.prototype.addStaticScheme = function(name,scheme) {
  this.maps[name] = scheme;
}

Colors.prototype.addDynScheme = function(name,scheme) {
  this.dyn[name] = scheme;
}

// small helper to clone an object
function clone(obj) {
  if (null == obj || "object" != typeof obj) return obj;
  var copy = obj.constructor();
  for (var attr in obj) {
    if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
  }
  return copy;
}
