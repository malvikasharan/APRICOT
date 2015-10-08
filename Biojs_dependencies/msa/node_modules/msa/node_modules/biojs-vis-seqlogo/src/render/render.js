var renderWithText = require("./render_with_text.js");
var renderWithRect = require("./render_with_rects.js");
var jbone = require("jbone");

// the main render function that draws the logo based on the provided options.
module.exports = function (options) {
  if (!this.data) {
    return;
  }
  options    = options || {};
  var zoom   = options.zoom || this.zoom,
  target = options.target || 1,
  scaled = options.scaled || null;
  var parent_width = this.dom_element.parent().attr('width'),
  max_canvas_width = 1,
  end = null,
  start = null,
  i = 0;

  /*
  if (target === this.previous_target) {
    return;
  }
  */

  this.previous_target = target;


  if (options.start) {
    this.start = options.start;
  }
  if (options.end) {
    this.end = options.end;
  }

  if (zoom <= 0.1) {
    zoom = 0.1;
  } else if (zoom >= 1) {
    zoom = 1;
  }

  this.zoom = zoom;

  end = this.end || this.data.heightArr.length;
  start = this.start || 1;
  end     = (end > this.data.heightArr.length) ? this.data.heightArr.length : end;
  end     = (end < start) ? start : end;

  start     = (start > end) ? end : start;
  start     = (start > 1) ? start : 1;

  this.y = this.height - 20;
  // Check to see if the logo will fit on the screen at full zoom.
  this.max_width = this.column_width * ((end - start) + 1);
  // If it fits then zoom out and disable zooming.
  if (parent_width > this.max_width) {
    zoom = 1;
    this.zoom_enabled = false;
  }
  this.zoom = zoom;

  this.zoomed_column = this.column_width * zoom;
  this.total_width = this.zoomed_column * ((end - start) + 1);

  // If zoom is not maxed and we still aren't filling the window
  // then ramp up the zoom level until it fits, then disable zooming.
  // Then we get a decent logo with out needing to zoom in or out.
  if (zoom < 1) {
    while (this.total_width < parent_width) {
      this.zoom += 0.1;
      this.zoomed_column = this.column_width * this.zoom;
      this.total_width = this.zoomed_column * ((end - start) + 1);
      this.zoom_enabled = false;
      if (zoom >= 1) {
        break;
      }
    }
  }

  if (target > this.total_width) {
    target = this.total_width;
  }
  this.dom_element.attr({'width': this.total_width + 'px'}).css({width: this.total_width + 'px'});

  this.canvas_width = this.total_width;
  var canvas_count = Math.ceil(this.total_width / this.canvas_width);
  this.columns_per_canvas = Math.ceil(this.canvas_width / this.zoomed_column);


  if (this.previous_zoom !== this.zoom) {
    this.dom_element.find('canvas').remove();
    this.previous_zoom = this.zoom;
    this.rendered = [];
  }

  this.canvases = [];
  this.contexts = [];


  for (i = 0; i < canvas_count; i++) {

    var split_start = (this.columns_per_canvas * i) + start,
    split_end   = split_start + this.columns_per_canvas - 1;
    if (split_end > end) {
      split_end = end;
    }

    var adjusted_width = ((split_end - split_start) + 1) * this.zoomed_column;

    if (adjusted_width > max_canvas_width) {
      max_canvas_width = adjusted_width;
    }

    var canv_start = max_canvas_width * i,
    canv_end = canv_start + adjusted_width;

    if (target < canv_end + (canv_end / 2) && target > canv_start - (canv_start / 2)) {
      // Check that we aren't redrawing the canvas and if not, then attach it and draw.
      //if (this.rendered[i] !== 1) {

        this.canvases[i] = attach_canvas(this.dom_element, this.height, adjusted_width, i, max_canvas_width);
        this.contexts[i] = this.canvases[i].getContext('2d');
        this.contexts[i].setTransform(1, 0, 0, 1, 0, 0);
        this.contexts[i].clearRect(0, 0, adjusted_width, this.height);
        this.contexts[i].fillStyle = "#ffffff";
        this.contexts[i].fillRect(0, 0, canv_end, this.height);


        if (this.zoomed_column > 12) {
          var fontsize = parseInt(10 * zoom, 10);
          fontsize = (fontsize > 10) ? 10 : fontsize;
          if (this.debug) {
            renderWithRect.call(this,split_start, split_end, i, 1);
          }
          renderWithText.call(this,split_start, split_end, i, fontsize);
        } else {
          renderWithRect.call(this,split_start, split_end, i);
        }
        //this.rendered[i] = 1;
      //}
    }

  }

  // check if the scroller object has been initialised and if not then do so.
  // we do this here as opposed to at object creation, because we need to
  // make sure the logo has been rendered and the width is correct, otherwise
  // we get a weird initial state where the canvas will bounce back to the
  // beginning the first time it is scrolled, because it thinks it has a
  // width of 0.
  if (!this.scrollme && this.options.scroller) {
    this.scrollme = new EasyScroller(this.dom_element[0], {
      scrollingX: 1,
      scrollingY: 0,
      eventTarget: this.called_on
    });
  }

  if (target !== 1) {
    this.scrollme.reflow();
  }
  return;
};


function attach_canvas(DOMid, height, width, id, canv_width) {
  var canvas = jbone(DOMid).find('#canv_' + id);

  if (!canvas.length) {
    jbone(DOMid).append('<canvas class="canvas_logo" id="canv_' + id + '"  height="' + height + '" width="' + width + '" style="left:' + canv_width * id + 'px"></canvas>');
    canvas = jbone(DOMid).find('#canv_' + id);
  }

  jbone(canvas).attr('width', width).attr('height', height);

  return canvas[0];
}
