/*
 * msa-seqtools
 * https://github.com/greenify/msa-seqtools
 *
 * Copyright (c) 2014 greenify
 * Licensed under the MIT license.
 */

var st = {};
module.exports = st;

// extract IDs and push them to the meta dict
st.getMeta = function(label) {
  if (st.contains(label, "|")) {
    var identifiers = label.split("|");
    var k = 0;
    var database, databaseID;
    var meta = {};
    while (k < identifiers.length - 1) {
      database = identifiers[k];
      databaseID = identifiers[k + 1];
      meta[database] = databaseID;
      k += 2;
    }
    // assume the last entry is the label
    var name = identifiers[identifiers.length - 1];
    // check whether there is a uniprot id
    if (name.indexOf("=") >= 0 && name.indexOf("OS") >= 0) {
      var ds = {};
      var details = name.split(" ");
      ds.en = details[0];
      details = details.splice(1);
      var nameLength = findSepInArr(details, "=");
      var detailsTmp = details.splice(nameLength - 1);
      name = details.join(" ");
      details = detailsTmp;
      k = 0;
      var block = [];
      details.forEach(function(item) {
        block.push(item);
        if (item.indexOf("=") >= 0) {
          strToDict(block.join(" "), "=", ds);
          block = [];
        }
      });
      return {
        name: name,
        ids: meta,
        details: ds
      };
    }
    return {
      name: name,
      ids: meta
    };
  }
  return {
    name: label
  };
};

var findSepInArr = function(arr, sep) {
  for (var i = 0; i < arr.lenght; i++) {
    if (arr[i].indexOf(i)) {
      return i;
    }
  }
  return arr.length - 1;
};

var strToDict = function(str, sep, toJoin) {
  toJoin = toJoin || {};
  var entries = str.split(sep);
  toJoin[entries[0].toLowerCase()] = entries[1];
  return toJoin;
};

var identDB = {
  "sp": {
    link: "http://www.uniprot.org/%s",
    name: "Uniprot"
  },
  "tr": {
    link: "http://www.uniprot.org/%s",
    name: "Trembl"
  },
  "gb": {
    link: "http://www.ncbi.nlm.nih.gov/nuccore/%s",
    name: "Genbank"
  },
  "pdb": {
    link: "http://www.rcsb.org/pdb/explore/explore.do?structureId=%s",
    name: "PDB"
  }
};

st.buildLinks = function(meta) {
  var links = {};
  meta = meta || {};
  Object.keys(meta).forEach(function(id) {
    if (id in identDB) {
      var entry = identDB[id];
      var link = entry.link.replace("%s", meta[id]);
      links[entry.name] = link;
    }
  });
  return links;
};


// search for a text
st.contains = function(text, search) {
  return ''.indexOf.call(text, search, 0) !== -1;
};

// split after e.g. 80 chars
st.splitNChars = function(txt, num) {
  var i, _ref;
  num = num || 80;
  var result = [];
  for (i = 0, _ref = txt.length - 1; i <= _ref; i += num) {
    result.push(txt.substr(i, num));
  }
  return result;
};

st.reverse = function(seq) {
  return seq.split('').reverse().join('');
}

st.complement = function(seq) {
  var newSeq = seq + "";
  var replacements = [
    // cg
    [/g/g, "0"],
    [/c/g, "1"],
    [/0/g, "c"],
    [/1/g, "g"],
    // CG
    [/G/g, "0"],
    [/C/g, "1"],
    [/0/g, "C"],
    [/1/g, "G"],
    // at
    [/a/g, "0"],
    [/t/g, "1"],
    [/0/g, "t"],
    [/1/g, "a"],
    // AT
    [/A/g, "0"],
    [/T/g, "1"],
    [/0/g, "T"],
    [/1/g, "A"],
  ];

  for(var rep in replacements){
    newSeq = newSeq.replace(replacements[rep][0], replacements[rep][1]);
  }
  return newSeq;
}

st.reverseComplement = function(seq){
  return st.reverse(st.complement(seq));
}

st.model = function Seq(seq, name, id) {
  this.seq = seq;
  this.name = name;
  this.id = id;
  this.ids = {};
};
