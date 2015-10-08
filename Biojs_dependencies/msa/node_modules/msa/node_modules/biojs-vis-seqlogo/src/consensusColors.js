module.exports = function ConsensusColors() {

  this.grey = '#7a7a7a';

  function arbitrate(threshold, scoreref) {
    var bestclass = '.',
    bestscore   = 0,
    type        = null,
    a           = null,
    b           = null,
    classSize = {
      '.' : 20,
      'h' : 11,
      '+' : 3,
      '-' : 2,
      'o' : 2,
      'p' : 2
    };

    for (type in scoreref) {
      if (scoreref.hasOwnProperty(type)) {
        if (scoreref[type] >= threshold) {
          a = classSize[type] || 1;
          b = classSize[bestclass] || 1;

          if (a < b) {
            bestclass = type;
            bestscore = scoreref[type];
          } else if (a === b) {
            if (scoreref[type] > bestscore) {
              bestclass = type;
              bestscore = scoreref[type];
            }
          }
        }
      }
    }
    return bestclass;
  }

  this.check_PG = function (pos, consensuses, colorsRef) {
    colorsRef[pos].P = '#ffff11';
    colorsRef[pos].G = '#ff7f11';
    return 1;
  };

  this.check_R = function (pos, consensuses, colorsRef) {
    colorsRef[pos].R = this.grey;

    var red = '#FF9999',
    letters = ['Q', 'K', 'R'],
    i = 0;

    for (i = 0; i < letters.length; i++) {
      if (consensuses['0.85'][pos] === letters[i]) {
        colorsRef[pos].R = red;
        return 1;
      }
    }

    if (consensuses['0.60'][pos] === '+' ||  consensuses['0.60'][pos] === 'R' || consensuses['0.60'][pos] === 'K') {
      colorsRef[pos].R = red;
      return 1;
    }
    return 1;
  };

  this.check_Q = function (pos, consensuses, colorsRef) {
    colorsRef[pos].Q = this.grey;

    var green = '#99FF99',
    letters = ['Q', 'T', 'K', 'R'],
    i = 0;

    if (consensuses['0.50'][pos] === 'b' ||
        consensuses['0.50'][pos] === 'E' ||
          consensuses['0.50'][pos] === 'Q') {
      colorsRef[pos].Q = green;
    return 1;
    }

    for (i = 0; i < letters.length; i++) {
      if (consensuses['0.85'][pos] === letters[i]) {
        colorsRef[pos].Q = green;
        return 1;
      }
    }

    if (consensuses['0.60'][pos] === '+' ||
        consensuses['0.60'][pos] === 'K' ||
          consensuses['0.50'][pos] === 'R') {
      colorsRef[pos].Q = green;
    return 1;
    }

    return 1;
  };

  this.check_N = function (pos, consensuses, colorsRef) {
    colorsRef[pos].N = this.grey;

    var green = '#99FF99';

    if (consensuses['0.50'][pos] === 'N') {
      colorsRef[pos].N = green;
      return 1;
    }

    if (consensuses['0.85'][pos] === 'D') {
      colorsRef[pos].N = green;
      return 1;
    }

    return 1;
  };

  this.check_K = function (pos, consensuses, colorsRef) {
    colorsRef[pos].K = this.grey;

    var red = '#FF9999',
    letters = ['K', 'R', 'Q'],
    i = 0;

    if (consensuses['0.60'][pos] === '+' ||
        consensuses['0.60'][pos] === 'R' ||
          consensuses['0.60'][pos] === 'K') {
      colorsRef[pos].K = red;
    return 1;
    }

    for (i = 0; i < letters.length; i++) {
      if (consensuses['0.85'][pos] === letters[i]) {
        colorsRef[pos].K = red;
        return 1;
      }
    }
    return 1;
  };

  this.check_E = function (pos, consensuses, colorsRef) {
    colorsRef[pos].E = this.grey;

    var red = '#FF9999',
    letters = ['D', 'E'],
    i = 0;

    if (consensuses['0.60'][pos] === '+' ||
        consensuses['0.60'][pos] === 'R' ||
          consensuses['0.60'][pos] === 'K') {
      colorsRef[pos].E = red;
    return 1;
    }

    for (i = 0; i < letters.length; i++) {
      if (consensuses['0.85'][pos] === letters[i]) {
        colorsRef[pos].E = red;
        return 1;
      }
    }

    if (consensuses['0.50'][pos] === 'b' ||
        consensuses['0.50'][pos] === 'E' ||
          consensuses['0.50'][pos] === 'Q') {
      colorsRef[pos].E = red;
    return 1;
    }

    return 1;
  };

  this.check_D = function (pos, consensuses, colorsRef) {
    colorsRef[pos].D = this.grey;

    var red = '#FF9999',
    letters = ['D', 'E', 'N'],
    i = 0;

    if (consensuses['0.60'][pos] === '+' ||
        consensuses['0.60'][pos] === 'R' ||
          consensuses['0.60'][pos] === 'K') {
      colorsRef[pos].D = red;
    return 1;
    }

    for (i = 0; i < letters.length; i++) {
      if (consensuses['0.85'][pos] === letters[i]) {
        colorsRef[pos].D = red;
        return 1;
      }
    }

    if (consensuses['0.50'][pos] === '-' ||
        consensuses['0.60'][pos] === 'E' ||
          consensuses['0.60'][pos] === 'D') {
      colorsRef[pos].D = red;
    return 1;
    }

    return 1;
  };

  this.check_ACFILMVW = function (pos, consensuses, colorsRef) {
    var aa = ['A', 'C', 'F', 'L', 'I', 'M', 'V', 'W'],
    caa = ['A', 'C', 'F', 'H', 'I', 'L', 'M', 'V', 'W', 'Y', 'P', 'Q', 'h'],
    i = 0,
    j = 0;

    for (i = 0; i < aa.length; i++) {
      colorsRef[pos][aa[i]] = this.grey;
      for (j = 0; j < caa.length; j++) {
        if (consensuses['0.60'][pos] === caa[j]) {
          colorsRef[pos][aa[i]] = '#9999FF';
        }
      }
    }
    return 1;
  };

  this.check_ST = function (pos, consensuses, colorsRef) {
    colorsRef[pos].S = this.grey;
    colorsRef[pos].T = this.grey;

    var letters = ['A', 'C', 'F', 'H', 'I', 'L', 'M', 'V', 'W', 'Y', 'P', 'Q'],
    i = 0;

    if (consensuses['0.50'][pos] === 'a' ||
        consensuses['0.50'][pos] === 'S' ||
          consensuses['0.50'][pos] === 'T') {
      colorsRef[pos].S = '#99FF99';
    colorsRef[pos].T = '#99FF99';
    return 1;
    }

    for (i = 0; i < letters.length; i++) {
      if (consensuses['0.85'][pos] === letters[i]) {
        colorsRef[pos].S = '#99FF99';
        colorsRef[pos].T = '#99FF99';
        return 1;
      }
    }
  };

  this.check_HY = function (pos, consensuses, colorsRef) {
    colorsRef[pos].H = this.grey;
    colorsRef[pos].Y = this.grey;

    var letters = ['A', 'C', 'F', 'H', 'I', 'L', 'M', 'V', 'W', 'Y', 'P', 'Q', 'h'],
    i = 0,
    cyan = '#99FFFF';

    if (consensuses['0.60'][pos] === 'h') {
      colorsRef[pos].H = cyan;
      colorsRef[pos].Y = cyan;
      return 1;
    }

    for (i = 0; i < letters.length; i++) {
      if (consensuses[0.85][pos] === letters[i]) {
        colorsRef[pos].H = cyan;
        colorsRef[pos].Y = cyan;
        return 1;
      }
    }

    return 1;
  };

  this.color_map = function (probs_array) {
    var thresholds = ['0.50', '0.60', '0.80', '0.85'],
    hydro = {
      'W': 1,
      'L': 1,
      'V': 1,
      'I': 1,
      'M': 1,
      'A': 1,
      'F': 1,
      'C': 1,
      'Y': 1,
      'H': 1,
      'P': 1
    },
    polar = { 'Q': 1,  'N': 1},
    positive = { 'K': 1, 'R': 1, 'H': 1 },
    alcohol  = { 'S': 1, 'T': 1 },
    negative = { 'E': 1, 'D': 1 },
    cons = {},
    colors = [],
    i = 0,
    c = 0,
    t = 0,
    a = 0,
    aa = [],
    column = null,
    score = {},
    consensusCol = null,
    threshold = null;


    for (c = 0; c < probs_array.length; c++) {
      column = probs_array[c];
      for (t = 0; t < thresholds.length; t++) {
        threshold = thresholds[t];
        score = {
          'p': 0,
          'o': 0,
          '-': 0,
          '+': 0,
          'h': 0
        };
        for (a = 0; a < column.length; a++) {
          aa = [];
          aa = column[a].split(':');
          score[aa[0]] = parseFloat(aa[1], 10);
          if (polar[aa[0]]) {
            score.p = score.p + parseFloat(aa[1], 10);
            continue;
          }

          if (alcohol[aa[0]]) {
            score.o = score.o + parseFloat(aa[1], 10);
            continue;
          }

          if (negative[aa[0]]) {
            score['-'] = score['-'] + parseFloat(aa[1], 10);
            continue;
          }

          if (positive[aa[0]]) {
            score['+'] = score['+'] + parseFloat(aa[1], 10);
          }

          if (hydro[aa[0]]) {
            score.h = score.h + parseFloat(aa[1], 10);
          }
        }
        consensusCol = arbitrate(threshold, score);
        if (!cons[threshold]) {
          cons[threshold] = [];
        }
        cons[threshold].push(consensusCol);
      }
    }

    for (i = 0; i < probs_array.length; i++) {
      colors[i] = {};
      this.check_D(i, cons, colors);
      this.check_R(i, cons, colors);
      this.check_Q(i, cons, colors);
      this.check_N(i, cons, colors);
      this.check_K(i, cons, colors);
      this.check_E(i, cons, colors);
      this.check_HY(i, cons, colors);
      this.check_ACFILMVW(i, cons, colors);
      //Colour alcohol.....
      this.check_ST(i, cons, colors);
      //Proline and Glycine get fixed colors....
      this.check_PG(i, cons, colors);
    }

    return colors;

  };
}
