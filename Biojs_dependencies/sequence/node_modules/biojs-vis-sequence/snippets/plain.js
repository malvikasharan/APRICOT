var Seq = require("biojs-vis-sequence");
var theSequence = '111111111122222222223333333333444444444455555555556666666666111111111122222222223333333333444444444455555555556666666666';
yourDiv.textContent = "";

var mySequence = new Seq({
  sequence: theSequence,
  target: yourDiv.id,
  format: 'CODATA',
  formatOptions: {
    header: false
  },
});

//@biojs-instance=mySequence
