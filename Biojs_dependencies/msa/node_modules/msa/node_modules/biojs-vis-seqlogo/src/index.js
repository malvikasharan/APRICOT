_ = require("underscore");

//var ConsensusColors = require("./consensusColors.js");
var canvasSupport = require("./canvasSupport.js");
var render = require("./render/render.js");
var Letter = require("./model/letter.js");
var view = require("backbone-viewj");
var axis = require("./axis");
var eventListener = require("./eventListener.js");
var settings = require("./info/settings.js");

var jbone = require("jbone");

module.exports = view.extend({

  options: {
    xaxis: true,
    yaxis: true,
    height: 300,
    column_width: 34,
    debug: true,
    scale_height_enabled: true,
    scaled_max: true,
    zoom_buttons: true,
    colorscheme: 'default',
    data: undefined,
    start: 1,
    end: undefined,
    zoom: 0.4,
    colors: undefined,
    divider: false,
    show_probs: false,
    divider_step: 5,
    show_divider: false,
    border: false,
    settings: false,
    scroller: true,
    positionMarker: true
  },

  loadDefault: function(options){
    this.data = options.data;

    // never show the alignment coordinates by default as that would get
    // really confusing.
    this.display_ali_map = 0;

    this.alphabet = options.data.alphabet || 'dna';

    this.start = options.start;
    //this.end = options.end || this.data.heightArr.length;
    this.zoom = parseFloat(options.zoom) || 0.4;
    this.default_zoom = this.zoom;

    this.column_width = options.column_width;
    this.height = options.height;
    this.canvas_width = 5000;
    this.scale_height_enabled = options.scale_height_enabled;

    // this needs to be set to null here so that we can initialise it after
    // the render function has fired and the width determined.
    this.scrollme = null;

    this.previous_target = 0;
    // keeps track of which canvas elements have been drawn and which ones haven't.
    this.rendered = [];
    this.previous_zoom = 0;

    if(this.data.max_height == undefined){
      this.data.max_height = this.calcMaxHeight(this.data.heightArr); 
    }

    // only show insert when we actually have the data
    if(!this.data.insert_probs || !this.data.delete_probs){
      this.options.show_probs = false;
    }

    if (options.scaled_max) {
      this.data.max_height = options.data.max_height_obs || this.data.max_height || 2;
    } else {
      this.data.max_height = options.data.max_height_theory || this.data.max_height || 2;
    }

    if(options.colors){
      this.changeColors(options.colors);
    }else{
      if (this.alphabet === 'aa') {
        this.aa_colors = require("./colors/aa.js");
        this.changeColors(this.aa_colors);
      }else{
        this.dna_colors = require("./colors/dna.js");
        this.changeColors(this.dna_colors);
      }
    }
  },
  initialize: function(options) {
    if (!canvasSupport()) {
      this.el.textContent = "Your browser doesn't support canvas.";
      return;
    }
    if(options.data == undefined){
      this.el.textContent = "No data added.";
    }

    // load default settings
    _.extend(this.options,options);
    var opt = this.options;
    this.loadDefault(opt);

    if(!this.options.show_probs){
      this.info_content_height = this.height;
    }else{
      // turn off the insert rows if the hmm used the observed or weighted processing flags.
      if (this.data.processing && /^observed|weighted/.test(this.data.processing)) {
        this.show_inserts = 0;
        this.info_content_height = this.height - 14;
      } else {
        this.show_inserts = 1;
        this.info_content_height = this.height - 44;
      }
    }
    this.$el = jbone(this.el);

    this.initDivs();

    if(this.options.settings){
      var form = settings(this,opt);
      this.$el.append(form);
    }

    eventListener(this.$el,this, this.logo_graphic);
    /*
       if (opt.columnInfo) {
       var columnInfo = require("./info/column_info.js");
       columnInfo(this);
       }
       */

  },
  initDivs: function(){
    var logo_graphic = mk("div");
    logo_graphic.className = "logo_graphic";
    this.logo_graphic = jbone(logo_graphic);

    var container = mk("div");
    container.className = "logo_container";
    container.style.height = this.height;
    this.container = jbone(container);

    this.container.append(logo_graphic);

    // add some internal divs for scrolling etc.
    this.$el.append(container);

    if(this.options.divider){
      var divider = mk("div");
      divider.className = "logo_divider";
      this.$el.append(divider);
    }

    this.dom_element = jbone(logo_graphic);
    this.called_on = this.$el;

    if(this.options.xaxis){
      axis.render_x_axis_label.call(this);
    }
    if(this.options.yaxis){
      axis.render_y_axis_label.call(this);
    }else{
      this.container[0].style.marginLeft = "0px";
    }

  },

  render: function(){
    render.call(this); 
    return this;
  },

  changeColors: function(colors){
    this.colors = colors;
    var bUseColorObject = (colors != undefined && colors.type != undefined);
    if(bUseColorObject){
      this.colorscheme = "dynamic";
    }
    this.buildAlphabet();
  },

  buildAlphabet: function(){
    /*
       if (this.alphabet === 'aa') {
       var probs_arr = this.data.probs_arr;
       if (probs_arr) {
       var cc = new ConsensusColors();
       this.cmap = cc.color_map(probs_arr);
       }
       }
       */

    //build the letter canvases
    this.letters = {};
    var colors = this.colors;
    if(this.colorscheme == "dynamic"){
      var tColors = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('');
      colors = {};
      tColors.forEach(function(e){
        colors[e] = "";
      });
    }
    for (var letter in colors) {
      if (colors.hasOwnProperty(letter)) {
        var loptions = {color: colors[letter]};
        this.letters[letter] = new Letter(letter, loptions);
      }
    }
  },

  toggleColorscheme: function (scheme) {
    // work out the current column we are on so we can return there
    var col_total = this.currentColumn();

    if (scheme) {
      if (scheme === 'default') {
        this.colorscheme = 'default';
      } else {
        this.colorscheme = 'consensus';
      }
    } else {
      if (this.colorscheme === 'default') {
        this.colorscheme = 'consensus';
      } else {
        this.colorscheme = 'default';
      }
    }

    // reset the rendered counter so that each section will re-render
    // with the new heights
    this.rendered = [];

    // re-flow and re-render the content
    this.scrollme.reflow();
    //scroll off by one to force a render of the canvas.
    this.scrollToColumn(col_total + 1);
    //scroll back to the location we started at.
    this.scrollToColumn(col_total);
  },

  toggleScale: function (scale) {
    // work out the current column we are on so we can return there
    var col_total = this.currentColumn();

    if (scale) {
      if (scale === 'obs') {
        this.data.max_height = this.data.max_height_obs;
      } else {
        this.data.max_height = this.data.max_height_theory;
      }
    } else {
      // toggle the max height
      if (this.data.max_height === this.data.max_height_obs) {
        this.data.max_height = this.data.max_height_theory;
      } else {
        this.data.max_height = this.data.max_height_obs;
      }
    }
    // reset the rendered counter so that each section will re-render
    // with the new heights
    this.rendered = [];
    //update the y-axis
    if(this.logoYAxis){
      this.logoYAxis.remove();
      //this.called_on.find('.logo_yaxis').remove();
    }
    axis.render_y_axis_label.call(this);

    // re-flow and re-render the content
    this.scrollme.reflow();
    //scroll off by one to force a render of the canvas.
    this.scrollToColumn(col_total + 1);
    //scroll back to the location we started at.
    this.scrollToColumn(col_total);
  },
  toggleAliMap: function (coords) {
    // work out the current column we are on so we can return there
    var col_total = this.currentColumn();

    if (coords) {
      if (coords === 'model') {
        this.display_ali_map = 0;
      } else {
        this.display_ali_map = 1;
      }
    } else {
      // toggle the max height
      if (this.display_ali_map === 1) {
        this.display_ali_map = 0;
      } else {
        this.display_ali_map = 1;
      }
    }
    axis.render_x_axis_label(this);

    // reset the rendered counter so that each section will re-render
    // with the new heights
    this.rendered = [];

    // re-flow and re-render the content
    this.scrollme.reflow();
    //scroll off by one to force a render of the canvas.
    this.scrollToColumn(col_total + 1);
    //scroll back to the location we started at.
    this.scrollToColumn(col_total);
  },

  currentColumn: function () {
    var before_left = this.scrollme.scroller.getValues().left,
    col_width = (this.column_width * this.zoom),
    col_count = before_left / col_width,
    half_visible_columns = (this.container.width() / col_width) / 2,
    col_total = Math.ceil(col_count + half_visible_columns);
    return col_total;
  },

  changeZoom: function (options) {
    var zoom_level = 0.3,
    expected_width = null;
    if (options.target) {
      zoom_level = options.target;
    } else if (options.distance) {
      zoom_level = (parseFloat(this.zoom) - parseFloat(options.distance)).toFixed(1);
      if (options.direction === '+') {
        zoom_level = (parseFloat(this.zoom) + parseFloat(options.distance)).toFixed(1);
      }
    }

    if (zoom_level > 1) {
      zoom_level = 1;
    } else if (zoom_level < 0.1) {
      zoom_level = 0.1;
    }

    // see if we need to zoom or not
    expected_width = (this.logo_graphic.width() * zoom_level) / this.zoom;
    if (expected_width > this.container.width()) {
      // if a center is not specified, then use the current center of the view
      if (!options.column) {
        //work out my current position
        var col_total = this.currentColumn();

        this.zoom = zoom_level;
        this.render({zoom: this.zoom});
        this.scrollme.reflow();

        //scroll to previous position
        this.scrollToColumn(col_total);
      } else { // center around the mouse click position.
        this.zoom = zoom_level;
        this.render({zoom: this.zoom});
        this.scrollme.reflow();

        var coords = this.coordinatesFromColumn(options.column);
        this.scrollme.scroller.scrollTo(coords - options.offset);
      }
    }
    return this.zoom;

  },

  columnFromCoordinates: function (x) {
    var column = Math.ceil(x / (this.column_width * this.zoom));
    return column;
  },

  coordinatesFromColumn: function (col) {
    var new_column = col - 1,
    x = (new_column  * (this.column_width * this.zoom)) + ((this.column_width * this.zoom) / 2);
    return x;
  },

  scrollToColumn: function (num, animate) {
    var half_view = (this.logo_container.width() / 2),
    new_left = this.coordinatesFromColumn(num);
    this.scrollme.scroller.scrollTo(new_left - half_view, 0, animate);
  },
  calcMaxHeight: function(columns){
    // loops over all columns and return the max height seen 
    return columns.reduce(function(m,c){
      var col = 0;
      for(var k in c){
        col += c[k];
      }
      return col > m ? col : m;
    },0);
  }


});

var mk = function(name){
  return document.createElement(name);
}
