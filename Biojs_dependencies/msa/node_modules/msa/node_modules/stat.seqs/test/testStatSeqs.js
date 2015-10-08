/*
 * stat.seqs
 * https://github.com/greenify/stat.seqs
 *
 * Copyright (c) 2014 greenify
 * Licensed under the MIT license.
 */

// chai is an assertion library
var chai = require('chai');

require("./mochaFix");

var assert = chai.assert;
var equal = assert.deepEqual;
var map = require("./mapHelper.js");

// requires your main app (specified in index.js)
var statProgram = require('..');
var stat;

beforeEach("prepare stat", function() {
  var seqs = ["AAABB",
    "ACCCB",
    "AATTC"
  ];
  stat = new statProgram(seqs);
});

describe('stat.seqs module', function() {

  describe('#wrong input()', function() {
    it('string input', function() {
      assert.throws(function() {
        statProgram("AA");
      }, TypeError);
    });
    it('no input', function() {
      assert.throws(function() {
        statProgram();
      }, TypeError);
    });
    //it('empty array', function(){
    //assert.throws(function(){statProgram([])},TypeError);
    //});
  });

  describe('#consensus()', function() {
    it('test default', function() {
      equal(stat.consensus(), "AAABB");
    });

    it('test different length', function() {

      var seqs = ["AAABB",
        "ACCCBCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      equal(stat.consensus(), "AAABBCC");
    });
  });

  describe('#identityCalc()', function() {
    it('test default', function() {
      equal(stat.identity(), [1, 0.4, 0.4]);
    });
    it('test different length', function() {

      var seqs = ["EAABB",
        "ACCCBCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundMap(stat.identity()), [0.8, 0.57, 0.4]);
    });

    it('different seq', function() {
      equal(stat.identity("AAAAA"), [0.6, 0.2, 0.4]);
    });
    it('do not cache the output', function() {
      equal(stat.identity("AAAAA"), [0.6, 0.2, 0.4]);
      equal(stat.identity(), [1, 0.4, 0.4]);
      equal(stat.identity("BBBBB"), [0.4, 0.2, 0.0]);
      equal(stat.identity("AAAAA"), [0.6, 0.2, 0.4]);
    });
  });

  describe('#backgmap.round()', function() {
    it('test default', function() {
      equal(map.roundMap(stat.background()), {
        A: 0.4,
        B: 0.2,
        C: 0.27,
        T: 0.13
      });
    });
    it('test different length', function() {

      var seqs = ["EAABB",
        "ACCCBCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundMap(stat.background()), {
        A: 0.29,
        B: 0.18,
        C: 0.35,
        T: 0.12,
        E: 0.06
      });
    });
  });

  describe('#gapCalc()', function() {
    it('test default', function() {
      equal(stat.gaps(), [0, 0, 0, 0, 0]);
    });
    it('test different length', function() {

      var seqs = [
        "-A-BB",
        "A-C-B-C",
        "A-CCBCC",
        "A--TC"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundArr(stat.gaps()), [0.25, 0.75, 0.5, 0.25, 0, 0.5, 0]);
    });
  });

  describe('#addSeqs()', function() {

    it('test different length', function() {

      equal(stat.consensus(), "AAABB");
      var seqs = [
        "AAABB",
        "ACCCB",
        "AATTC"
      ];
      stat.resetSeqs(seqs);
      equal(stat.consensus(), "AAABB");
      stat.addSeq("AATTC");
      equal(stat.consensus(), "AATTB");
      stat.addSeqs(["AAABB", "AAABB"]);
      equal(stat.consensus(), "AAABB");
    });
  });

  describe('#maxLength()', function() {

    it('test length change', function() {
      equal(stat.maxLength(), 5);
      stat.addSeq("AATTCO");
      equal(stat.maxLength(), 6);
    });

    it('test with an array', function() {
      stat.addSeqs(["AAABBTT", "AAABB"]);
      equal(stat.maxLength(), 7);
    });
  });

  describe('#removeSeq()', function() {

    it('test remove by string', function() {
      equal(stat.maxLength(), 5);
      stat.addSeq("AATTCO");
      equal(stat.maxLength(), 6);
      stat.removeSeq("AATTCO");
      equal(stat.maxLength(), 5);
    });

    it('test remove by arr', function() {
      stat.addSeqs(["AAABBTT", "AAABB"]);
      equal(stat.maxLength(), 7);
      stat.removeSeq(3);
      equal(stat.maxLength(), 5);
    });
  });

  describe('#frequency()', function() {
    it('test default', function() {
      equal(map.roundArrMap(stat.frequency()), [{
        A: 1
      }, {
        A: 0.67,
        C: 0.33
      }, {
        A: 0.33,
        C: 0.33,
        T: 0.33
      }, {
        B: 0.33,
        C: 0.33,
        T: 0.33
      }, {
        B: 0.67,
        C: 0.33
      }]);
    });
    it('test different length', function() {

      var seqs = ["EAABB",
        "ACCCBCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);
      equal(map.roundArrMap(stat.frequency()), [{
        E: 0.33,
        A: 0.67
      }, {
        A: 0.67,
        C: 0.33
      }, {
        A: 0.33,
        C: 0.33,
        T: 0.33
      }, {
        B: 0.33,
        C: 0.33,
        T: 0.33
      }, {
        B: 0.67,
        C: 0.33
      }, {
        C: 1
      }, {
        C: 1
      }]);
    });
  });

  describe('#ic()', function() {
    it('test default', function() {
      equal(map.roundMap(stat.ic()), [0, 0.92, 1.58, 1.58, 0.92]);
    });
    it('test different length', function() {

      var seqs = ["GAABB",
        "ACCCGCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundMap(stat.ic()), [0.92, 0.92, 1.58, 1.58, 1.58, 0, 0]);
    });
    it('test with gaps', function() {

      var seqs = ["GAABB",
        "--CCGCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundMap(stat.ic()), [1, 0, 1.58, 1.58, 1.58, 0, 0]);
    });

    it('gaps shouldnt change the ic', function() {

      var seqs = ["A",
        "A",
        "A",
        "-"
      ];
      stat.resetSeqs(seqs);
      equal(map.roundMap(stat.ic()), [0]);

      seqs = ["A",
        "A",
        "A",
        "-",
        "-",
        "-",
        "-"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundMap(stat.ic()), [0]);
    });


    it('scaled', function() {
      equal(map.roundMap(stat.scale(stat.ic())), [0, 0.46, 0.79, 0.79, 0.46]);
    });
  });

  describe('#conservation()', function() {
    it('test default', function() {
      equal(map.roundMap(stat.conservation()), [2, 1.08, 0.42, 0.42, 1.08]);
    });
    it('test different length', function() {

      var seqs = ["GAABB",
        "ACCCGCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      equal(map.roundMap(stat.conservation()), [1.08, 1.08, 0.42, 0.42, 0.42, 2, 2]);
    });

    it('scaled', function() {
      equal(map.roundMap(stat.scale(stat.conservation())), [1, 0.54, 0.21, 0.21, 0.54]);
    });
  });


  describe('#conservation per letter()', function() {
    it('test default', function() {
      var res = map.roundMapMap(stat.conservResidue());
      equal(res, [{
        A: 2
      }, {
        A: 0.72,
        C: 0.36
      }, {
        A: 0.14,
        C: 0.14,
        T: 0.14
      }, {
        B: 0.14,
        C: 0.14,
        T: 0.14
      }, {
        B: 0.72,
        C: 0.36
      }]);
    });
    it('test different length', function() {

      var seqs = ["GAABB",
        "ACCCGCC",
        "AATTC"
      ];
      stat.resetSeqs(seqs);

      var res = map.roundMapMap(stat.conservResidue());
      equal(res, [{
        G: 0.36,
        A: 0.72
      }, {
        A: 0.72,
        C: 0.36
      }, {
        A: 0.14,
        C: 0.14,
        T: 0.14
      }, {
        B: 0.14,
        C: 0.14,
        T: 0.14
      }, {
        B: 0.14,
        G: 0.14,
        C: 0.14
      }, {
        C: 2
      }, {
        C: 2
      }]);
    });

    it('scaled', function() {
      var res = map.roundMapMap(stat.conservResidue({
        scaled: true
      }));
      equal(res, [{
        A: 1
      }, {
        A: 0.36,
        C: 0.18
      }, {
        A: 0.07,
        C: 0.07,
        T: 0.07
      }, {
        B: 0.07,
        C: 0.07,
        T: 0.07
      }, {
        B: 0.36,
        C: 0.18
      }]);
    });

    it('scaled with gaps', function() {

      var seqs = [
        "ACA-",
        "AT--",
        "----",
        "----"
      ];
      stat = new statProgram(seqs, {useGaps: true});
      var res = map.roundMapMap(stat.conservResidue({
        scaled: true
      }));
      equal(res, [{
        A: 0.5
      }, {
        C: 0.13,
        T: 0.13
      },{
        A: 0.25
      }, {
      }]);
      // reset to default
      stat = new statProgram(seqs);
    });

    it('scaled with gaps ii', function() {

      var seqs = [
        "ACA-",
        "AC--",
        "AT--",
        "----",
        "----"
      ];
      stat = new statProgram(seqs, {useGaps: true});
      var res = map.roundMapMap(stat.conservResidue({
        scaled: true
      }));
      equal(res, [{
        A: 0.6
      }, {
        C: 0.22,
        T: 0.11
      },{
        A: 0.2
      }, {
      }]);
      // reset to default
      stat = new statProgram(seqs);
    });



  });


});

