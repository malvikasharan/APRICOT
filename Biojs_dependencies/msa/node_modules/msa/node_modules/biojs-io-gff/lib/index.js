/*
 * biojs-io-gff
 * https://github.com/greenify/biojs-io-gff
 *
 * Copyright (c) 2014 greenify
 * Licensed under the Apache 2 license.
 */

var parser = require("biojs-io-parser");

var gff = function() {};
parser.mixin(gff);

module.exports = gff;

var utils = require("./utils");
var jalview = require("./jalview");

/**
 * Method responsible to parse GFF
 * @see https://www.sanger.ac.uk/resources/software/gff/spec.html#t_2
 *
 * @example
 *
 *     biojsiogff.parse('SEQ1  EMBL  atg  103  105  .  +  0');
 *
 * @method parse
 * @param {String} file GFF file
 * @return {String} Returns JSON representation
 */

gff.parseLines = function(file) {
  var lines = file.split("\n");
  var config = {};
  var arr = [];
  config.type = gff._guessType(lines);
  var offset = 0;
  if (config.type === "jalview") {
    var ret = jalview.readHeader(lines);
    //console.log(ret);
    offset = ret.offset;
    config.colors = ret.colors;
    arr = ret.features;
  }
  for (var i = offset; i < lines.length; i++) {
    // ignore comments for now
    var line = lines[i];
    if (line.length === 0 || line[0] === "#")
      continue;

    line = gff.parseLine(line);
    if (line !== undefined)
      arr.push(line);
  }
  return {
    features: arr,
    config: config
  };
};

gff._guessType = function(line) {
  if (line[0].substring(0, 15) === "##gff-version 3") {
    return "gff3";
  } else if (line[0].indexOf("#") < 0 && line[0].split("\t").length === 2) {
    // no comments and two columns. let's hope this is from jalview
    return "jalview";
  }
  // unable to read file header. lets hope this is gff3
  return "gff3";
};

/**
 * parses GFF and returns a dictionary of all seqs with their features
 * @method parseSeqs
 * @param {String} file GFF file
 * @return {String} Returns dictionary of sequences with an array of their features
 */
gff.parseSeqs = gff.parse = function(file) {
  var obj = gff.parseLines (file);
  var seqs = {};
  obj.features.forEach(function(entry) {
    var key = entry.seqname;
    if (seqs[key] === undefined) seqs[key] = [];
    delete entry.seqname;
    seqs[key].push(entry);
  });
  delete obj.features;
  obj.seqs = seqs;
  return obj;
};

/*
 * parses one GFF line and returns it
 */
gff.parseLine = function(line) {
  var tLine = {};

  var columns = line.split(/\s+/);
  // ignore empty lines
  if (columns.length === 1)
    return;

  tLine.seqname = columns[0];
  tLine.source = columns[1];
  tLine.feature = columns[2];
  tLine.start = parseInt(columns[3]);
  tLine.end = parseInt(columns[4]);
  tLine.score = columns[5]; // only DNA,RNA
  tLine.strand = columns[6]; // only DNA,RNA
  tLine.frame = columns[7]; // only DNA,RNA
  var attr = columns.slice(8).join(" "); // plain text comments

  // remove undefined (dot)
  Object.keys(tLine).forEach(function(key) {
    if (tLine[key] === ".") {
      tLine[key] = undefined;
    }
  });

  // parse optional parameters
  if (tLine.score) {
    tLine.score = parseFloat(tLine.score);
  }
  if (tLine.frame) {
    tLine.frame = parseInt(tLine.frame);
  }

  tLine.attributes = utils.extractKeys(attr);
  return tLine;
};

gff.exportLine = function(line) {
  var attrs = Object.keys(line.attributes).map(function(key) {
    return key + "=" + line.attributes[key];
  }).join(";");
  var cells = [line.seqname, line.source, line.feature, line.start, line.end, line.score,
    line.strand, line.frame, attrs
  ];
  cells = cells.map(function(e) {
    if (e === undefined) {
      return ".";
    }
    return e;
  });
  return cells.join("\t");
};

gff.exportLines = function(lines) {
  return "##gff-version 3\n" + lines.map(gff.exportLine).join("\n");
};

gff.exportSeqs = gff.export = function(seqs) {
  var lines = [];
  var pLine = function(e) {
    e.seqname = key;
    lines.push(e);
  };

  for (var key in seqs) {
    seqs[key].forEach(pLine);
  }
  return gff.exportLines(lines);
};
