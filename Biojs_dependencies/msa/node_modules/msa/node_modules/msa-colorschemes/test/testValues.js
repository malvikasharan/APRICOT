var chai = require('chai');
var assert = chai.assert;
var equal = assert.deepEqual;
var schemes = require("..");
var schemeMgr;

require("./mochaFix");

beforeEach("prepare stat", function(){
  schemeMgr = new schemes();
});

describe('color schemes module', function(){

  describe('#static function()', function(){
    it('should be accessible ', function(){
      var Clustal = schemes.getScheme("clustal");
      equal(Clustal["B"], "#fff");
    });
  });

  describe('#schememgr()', function(){
    it('should be accessible ', function(){
      var Clustal = schemeMgr.getScheme("clustal");
      equal(Clustal.getColor("B"), "#fff");
      equal(Clustal.type, "static");
      equal(Clustal.defaultValue, "#ffffff");
    });

    it('should allow schemes to be added', function(){
      schemeMgr.addStaticScheme("bscheme", {B: "#bbb"})
      var Clustal = schemeMgr.getScheme("bscheme");
      equal(Clustal.type, "static");
      equal(Clustal.getColor("B"), "#bbb");
    });

    it('should allow dynamic schemes', function(){
      var fun = function(letter,info){
        return info.pos % 2 == 0 ? "#ccc" : "#ddd";
      }
      schemeMgr.addDynScheme("fscheme",fun)

      var scheme = schemeMgr.getScheme("fscheme")
      equal(scheme.type, "dyn");
      equal(scheme.getColor("B", {pos: 1}), "#ddd");
      equal(scheme.getColor("B", {pos: 2}), "#ccc");
    });
  });
});
