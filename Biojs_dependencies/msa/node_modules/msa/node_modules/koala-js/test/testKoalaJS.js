var chai = require("chai");
var assert = chai.assert;
var equal = assert.deepEqual;

var l = require("..");

require("./mochaFix.js");

suite("Koala-JS");

test("default values", function(){
  obj = {a: 42};
  equal(l.d(obj.a, 0), 42);
  equal(l.d(obj.b, 0), 0);
});

