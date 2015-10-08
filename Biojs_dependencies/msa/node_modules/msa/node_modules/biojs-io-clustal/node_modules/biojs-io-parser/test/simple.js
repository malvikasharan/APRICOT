var Parser = require('../');

var chai = require("chai");
var assert = chai.assert;
var equal = assert.equal;
var nock = require('nock');

var testUrl = 'http://an.url';

var scope = nock(testUrl)
  .persist()
  .get('/foo')
  .reply(200, "ok");

suite("Through parser");

var throughParser = function() {
  this.parse = function(data) {
    return data;
  };
  Parser.mixin(this);
};

test('Should return the same file on read of urls', function(done) {
  var sparser = new throughParser();
  sparser.read(testUrl + "/foo", function(err, body) {
    equal(body, "ok");
    equal(err, undefined);
    done();
  });
});

test('Should support extend of objects', function(done) {
  var throughParserAlt = {
    parse: function(data) {
      return data;
    }
  };
  Parser.mixin(throughParserAlt);

  var sparser = throughParserAlt;
  sparser.read(testUrl + "/foo", function(err, body) {
    equal(body, "ok");
    equal(err, undefined);
    done();
  });
});

test('Should return a promise if the callback is undefined ', function(done) {
  var sparser = new throughParser();
  sparser.read(testUrl + "/foo").then(function(body) {
    equal(body, "ok");
    done();
  },function(){
    assert.fail("err");
    done();
  });
});


