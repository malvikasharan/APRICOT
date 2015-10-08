# The Sequence Component #

For a working example, please go to [JSBin](http://jsbin.com/jixehituxopa/1/edit)

## Instantiation ##
1 Get the main JS file from [npm](https://www.npmjs.com/package/biojs-vis-sequence) 

2 Remember to add the required JS files, i.e., the Sequence Component, jQuery, and jQuery browser plugin. Something like: 
```
    <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script type="text/javascript">
    jQuery = $;
    </script>
    <script src="../js/biojs-vis-sequence.js"></script>
    <script src="../js/jquery-browser-plugin.js"></script>
```
3 Create a div tag which holds an unique identifier.
```
    <body>
    ...
    	<div id="YourOwnDivId" />
    ...
    </body>
```
4 Create a code snippet within a script tag and create and instance of biojs-vis-sequence.
```
var Sequence = require("biojs-vis-sequence");
window.onload = function() {
var theSequence = "METLCQRLNVCQDKILTHYENDSTDLRDHIDYWKHMRLECAIYYKAREMGFKHINHQVVPTLAVSKNKALQAIELQLTLETIYNSQYSNEKWTLQDVSLEVYLTAPTGCIKKHGYTVEVQFDGDICNTMHYTNWTHIYICEEAojs SVTVVEGQVDYYGLYYVHEGIRTYFVQFKDDAEKYSKNKVWEVHAGGQVILCPTSVFSSNEVSSPEIIRQHLANHPAATHTKAVALGTEETQTTIQRPRSEPDTGNPCHTTKLLHRDSVDSAPILTAFNSSHKGRINCNSNTTPIVHLKGDANTLKCLRYRFKKHCTLYTAVSSTWHWTGHNVKHKSAIVTLTYDSEWQRDQFLSQVKIPKTITVSTGFMSI";
var mySequence = new Sequence({
        sequence : theSequence,
        target : "YourOwnDivId",
        format : 'CODATA',
        id : 'P918283',
        annotations: [
       		{ 
				name:"CATH",
            	color:"#F0F020",
            	html: "Using color code #F0F020 ",
            	regions: [{start: 122, end: 135}]
          	},{ 
				name:"TEST",
         		html:"<br> Example of <b>HTML</b>",
         		color:"green",
         		regions: [
           			{start: 285, end: 292},
           			{start: 293, end: 314, color: "#2E4988"}
				]
       		}
     	],
     	highlights : [
        	{ start:30, end:42, color:"white", background:"green", id:"spin1" },
	        { start:139, end:140 },
    	    { start:631, end:633, color:"white", background:"blue" }
     	]
	});
};
```

## Options ##

### Required Parameters ###
- target | {string}

Identifier of the DIV tag where the component should be displayed.

- sequence | {string}

The sequence to be displayed.

### Optional Parameters ###
- id | {string}

Sequence identifier if apply.

- format | {string}

The display format for the sequence representation.
Default: "FASTA"

- highlights | {Object[]}

For highlighting multiple regions. Syntax:
```
[
 // Highlight aminoacids from 'start' to 'end' of the current strand using the specified 'color' (optional) and 'background' (optional).
 { start: <startVal1>, end: <endVal1> [, id:<idVal1>] [, color: <HTMLColor>] [, background: <HTMLColor>]},
 //
 // Any others highlights
 ..., 
 //
 { start: <startValN>, end: <endValN> [, id:<idValN>] [, color: <HTMLColor>] [, background: <HTMLColor>]}
]
```

-- **Example : **
```
highlights : [
        { start:30, end:42, color:"white", background:"green", id:"spin1" },
        { start:139, end:140 },
        { start:631, end:633, color:"white", background:"blue" }
    ]
```

- columns | {Object}

Options for displaying the columns. Syntax: 
```
{ size: <numCols>, spacedEach: <numCols>}
Default: {size:40,spacedEach:10}
```
- selection | {Object}

Positions for the current selected region. Syntax: 
```
{ start: <startValue>, end: <endValue>}
```

- annotations | {Object[]}

Set of overlapping annotations. Must be an array of objects following the syntax: 
```
[
  // An annotation:
  { name: <name>,
    html: <message>,
    color: <color_code>,
    regions: [{ start: <startVal1>, end: <endVal1> color: <HTMLColor>}, ...,{ start: <startValN>, end: <endValN>, color: <HTMLColor>}]
  },
   
  // ...
  // more annotations here
  // ...
]
```
where:

-- name is the unique name for the annotation
-- html is the message (can be HTML) to be displayed in the tool tip.
-- color is the default HTML color code for all the regions.
-- regions array of objects defining the intervals which belongs to the annotation.
-- regions[i].start is the starting character for the i-th interval.
-- regions[i].end is the ending character for the i-th interval.
-- regions[i].color is an optional color for the i-th interval. 

- formatOptions | {Object} 
 
Options for displaying the title. by now just affecting the CODATA format. Syntax:
```
formatOptions : {
    title:false,
    footer:false
}

Default
formatOptions : {
    title:true,
    footer:true
}
```

### Methods ###
- addAnnotation

Annotate a set of intervals provided in the argument.

-- **Parameters : **

{Object} annotation

The intervals belonging to the same annotation. Syntax: { name: <value>, color: <HTMLColorCode>, html: <HTMLString>, regions: [{ start: <startVal1>, end: <endVal1>}, ..., { start: <startValN>, end: <endValN>}] }

-- **Example : **
```	
// Annotations using regions with different colors.
mySequence.addAnnotation({
   name:"UNIPROT",
   html:"<br> Example of <b>HTML</b>",
   color:"green",
   regions: [
      {start: 540, end: 560},
      {start: 561, end:580, color: "#FFA010"},
      {start: 581, end:590, color: "red"},
      {start: 690, end:710}]
});
```

- addHighlight

Highlights a region using the font color defined in {Biojs.Sequence#highlightFontColor} by default is red.

-- **Parameters : **

{Object} h

The highlight defined as follows:

-- **Example : **
```
// highlight the characters within the position 100 to 150, included.

mySequence.addHighlight( { "start": 100, "end": 150, "color": "white", "background": "red", "id": "aaa" } );

Returns:

    {int} representing the id of the highlight on the internal array. Returns -1 on failure
```

- clearSequence

Shows the columns indicated by the indexes array.

-- **Parameters : **

{string} showMessage Optional

Message to be showed.

{string} icon Optional

Icon to be showed a side of the message

-- **Example : **
```	
mySequence.clearSequence("No sequence available", "../biojs/css/images/warning_icon.png");
```

- formatSelectorVisible

Set the visibility of the drop-down list of formats.

-- **Parameters : **

{boolean} visible

true: show; false: hide.


- hide

Hides the whole component.


- hideFormatSelector

This is similar to a {Biojs.Protein3D#formatSelectorVisible} with the 'false' argument.

-- **Example : **
```
// Hides the format selector.
mySequence.hideFormatSelector();
```

- highlight

Highlights a region using the font color defined in {Biojs.Protein3D#highlightFontColor} by default is red.

-- **Parameters : **

{int} start

The starting character of the highlighting.

{int} end

The ending character of the highlighting.

{string} color Optional

HTML color code.

{string} background Optional

HTML color code.

{string} id Optional

Custom identifier.

Returns:

{int} representing the id of the highlight on the internal array. Returns -1 on failure


- removeAllAnnotations

Removes all the current annotations.

-- **Example : **
```
mySequence.removeAllAnnotations();
```

- removeAllHighlights

Remove all the highlights of whole sequence.

-- **Example : **
```	
mySequence.removeAllHighlights();
```

- removeAnnotation

Removes an annotation by means of its name.

-- **Parameters : **

{string} name

The name of the annotation to be removed.

-- **Example : **
```
// Remove the UNIPROT annotation.
mySequence.removeAnnotation('UNIPROT');
```

- removeHighlight

Remove a highlight.

-- **Parameters : **

{string} id

The id of the highlight on the internal array. This value is returned by method highlight.

-- **Example : **
```	
// Clear the highlighted characters within the position 100 to 150, included.
mySequence.removeHighlight("spin1");
```

- setAnnotation

Annotate a set of intervals provided in the argument.

-- **Parameters : **

{Object} annotation

The intervals belonging to the same annotation. Syntax: 

{ name: <value>, color: <HTMLColorCode>, html: <HTMLString>, regions: [{ start: <startVal1>, end: <endVal1>}, ..., { start: <startValN>, end: <endValN>}] }

- setFormat

Changes the current displaying format of the sequence.

-- **Parameters : **

{string} format

The format for the sequence to be displayed.

-- **Example : **
```	
// Set format to 'FASTA'.
mySequence.setFormat('FASTA');
```

- setNumCols

Changes the current number of columns in the displayed sequence.

-- **Parameters : **

{int} numCols

The number of columns.

-- **Example : **
```	
// Set the number of columns to 70.
mySequence.setNumCols(70);
```

- setSelection

Set the current selection in the sequence causing the event Biojs.Sequence#onSelectionChanged

-- **Parameters : **

{int} start

The starting character of the selection.

{int} end

The ending character of the selection

-- **Example : **
```	
// set selection from the position 100 to 150
mySequence.setSelection(100, 150);
```

- setSequence

Shows the columns indicated by the indexes array.

-- **Parameters : **

{string} seq

The sequence strand.

{string} identifier Optional

Sequence identifier.

-- **Example : **
```
mySequence.setSequence("P99999");
```

- show

Shows the whole component.

- showFormatSelector

This is similar to a {Biojs.Protein3D#formatSelectorVisible} with the 'true' argument.

-- **Example : **
```
// Shows the format selector.
mySequence.showFormatSelector();
```

- unHighlight

Clear a highlighted region using.

-- **Parameters : **

{int} id

The id of the highlight on the internal array. This value is returned by method highlight.

- unHighlightAll

Clear the highlights of whole sequence. 

### Events ###
- onAnnotationClicked

-- **Parameters : **

{function} actionPerformed

An function which receives an Biojs.Event object as argument.

Returned data in the Biojs.Event object:

{Object} source

The component which did triggered the event.

{string} type

The name of the event.

{string} name

The name of the selected annotation.

{int} pos

A number indicating the position of the selected amino acid.


-- **Example : **
```	
mySequence.onAnnotationClicked(
   function( objEvent ) {
      alert("Clicked " + objEvent.name + " on position " + objEvent.pos );
   }
);
```

- onSelectionChange

-- **Parameters : **

{function} actionPerformed

An function which receives an Biojs.Event object as argument.

Returned data in the Biojs.Event object:

{Object} source

The component which did triggered the event.

{string} type

The name of the event.

{int} start

A number indicating the start of the selection.

{int} end

A number indicating the ending of selection.


-- **Example : **
```	
mySequence.onSelectionChange(
   function( objEvent ) {
      alert("Selection in progress: " + objEvent.start + ", " + objEvent.end );
   }
);
```

- onSelectionChanged

-- **Parameters : **

{function} actionPerformed

An function which receives an Biojs.Event object as argument.

Returned data in the Biojs.Event object:

{Object} source

The component which did triggered the event.

{string} type

The name of the event.

{int} start

A number indicating the start of the selection.

{int} end

A number indicating the ending of selection.


-- **Example : **
```	
mySequence.onSelectionChanged(
   function( objEvent ) {
      alert("Selected: " + objEvent.start + ", " + objEvent.end );
   }
);
```
