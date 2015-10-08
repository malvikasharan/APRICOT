/*
 * biojs-io-gff
 * https://github.com/greenify/biojs-io-gff
 *
 * Copyright (c) 2014 greenify
 * Licensed under the Apache 2 license.
 */

var chai = require('chai');
var assert = chai.assert;
var equal = assert.deepEqual;

var gff = require('../');
var utils= require('../lib/utils');
var fs = require('fs');

suite("GFF parser");

test("test with fs", function(done) {
  var expectedResult = JSON.parse(fs.readFileSync(__dirname + '/dummy.json', 'utf8'));
  fs.readFile(__dirname + '/dummy.gff','utf8', function(err,data){
    if (err) return assert.fail(err);
    var obj = gff.parseLines(data).features;
    obj = JSON.parse(JSON.stringify(obj));
    equal(obj[0], expectedResult[0]);
    done();
  });
});

test("test with fer1", function(done) {
  var expectedResult = JSON.parse(fs.readFileSync(__dirname + '/fer1.json', 'utf8'));
  fs.readFile(__dirname + '/fer1.gff','utf8', function(err,data){
    if (err) return assert.fail(err);
    var obj = gff.parseLines(data).features;
    obj = JSON.parse(JSON.stringify(obj));
    equal(obj[0], expectedResult[0]);
    done();
  });
});

test("test with eden", function(done) {
  var expectedResult = JSON.parse(fs.readFileSync(__dirname + '/eden.json', 'utf8'));
  fs.readFile(__dirname + '/eden.gff3','utf8', function(err,data){
    if (err) return assert.fail(err);
    var obj = gff.parseLines(data).features;
    obj = JSON.parse(JSON.stringify(obj));
    equal(obj[0], expectedResult[0]);
    done();
  });
});

test("test import/export", function(done) {
  fs.readFile(__dirname + '/import.gff3','utf8', function(err,data){
    if (err) return assert.fail(err);
    var obj = gff.parseLines(data).features;
    equal(gff.exportLines(obj).split("\n"), data.split("\n").filter(function(e){
     return e;                                                              
    }));
    done();
  });
});

test("test import/export: seqs", function(done) {
  fs.readFile(__dirname + '/import.gff3','utf8', function(err,data){
    if (err) return assert.fail(err);
    var obj = gff.parseSeqs(data).seqs;
    equal(gff.exportSeqs(obj).split("\n"), data.split("\n").filter(function(e){
     return e;                                                              
    }));
    done();
  });
});


test("test with jalview", function(done) {
  var expectedResult = JSON.parse(fs.readFileSync(__dirname + '/eden.json', 'utf8'));
  fs.readFile(__dirname + '/feature.jalview','utf8', function(err,data){
    if (err) return assert.fail(err);
    var obj = gff.parseLines(data);
    var features = JSON.parse(JSON.stringify(obj.features));
    equal("#009ba5", obj.config.colors["signal peptide"]);
    equal(9, Object.keys(obj.config.colors).length);
    equal("jalview", obj.config.type);
    equal(obj.features.length, 10);
    //equal(obj[0], expectedResult[0]);
    done();
  });
});


test("test rgb", function() {
  equal(utils.rgbToHex([0,0,0]), "#000000");
  equal(utils.rgbToHex([0,65,0]), "#004100");
  equal(utils.rgbToHex([0,65,77]), "#00414d");
  equal(utils.rgbToHex([123,65,77]), "#7b414d");
  equal(utils.rgbToHex([255,255,255]), "#ffffff");
});

test("test with features", function(done) {
  fs.readFile(__dirname + '/eden.gff3','utf8', function(err,data){
    if (err) return console.log(err);
    var obj = gff.parseSeqs(data).seqs;
    equal(1, Object.keys(obj).length);
    equal(23, obj.ctg123.length);
    done();
  });
});

