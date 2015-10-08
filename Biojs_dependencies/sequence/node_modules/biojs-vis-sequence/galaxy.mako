var Seq = require("biojs-vis-sequence");
var Fasta = require("biojs-io-fasta");

galaxy.getData(function(data, req){

	var seqs = Fasta.parse(data);

	// this component can only display one sequence
	var seq  = seqs[0];
    var mySequence = new Seq({
      sequence : seq.seq,
      target : galaxy.el,
      format : 'CODATA',
      formatOptions : {
        title:false,
        footer:false
      },
      id : 'P918283'
    });
});
