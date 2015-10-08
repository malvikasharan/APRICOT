var draw_border = require("./draw/border.js");
var draw_ticks = require("./draw/ticks.js");
var draw_column_number = require("./draw/column_number.js");

module.exports = function (start, end, context_num, borders) {
  var x = 0,
  column_num = start,
  column_label = null,
  i = 0,
  top_height = Math.abs(this.data.max_height),
  bottom_height = Math.abs(this.data.min_height_obs),
  total_height = top_height + bottom_height,
  top_percentage    = Math.round((Math.abs(this.data.max_height) * 100) / total_height),
  //convert % to pixels
  top_pix_height = Math.round((this.info_content_height * top_percentage) / 100),
  bottom_pix_height = this.info_content_height - top_pix_height,
  mod = 10;


  for (i = start; i <= end; i++) {
    if (this.data.mmline && this.data.mmline[i - 1] === 1) {
      this.contexts[context_num].fillStyle = '#cccccc';
      this.contexts[context_num].fillRect(x, 10, this.zoomed_column, this.height - 40);
    } else {
      var column = this.data.heightArr[i - 1],
      previous_height = 0,
      previous_neg_height = top_pix_height,
      letters = column.length,
      j = 0;
      for(var j in column){
        values = [j,column[j]];
        if (values[1] > 0.01) {
          var letter_height = parseFloat(values[1]) / this.data.max_height,
          x_pos = x,
          glyph_height = (this.info_content_height - 2) * letter_height,
          y_pos = (this.info_content_height - 2) - previous_height - glyph_height,
          color = null;


          if(this.colorscheme === 'dynamic'){
            color = this.colors.getColor(values[0], {pos: i - 1} )
          }else{
            if(this.colorscheme === 'consensus') {
              color = this.cmap[i - 1][values[0]] || "#7a7a7a";
            } else {
              color = this.colors[values[0]];
            }
          }

          if (borders) {
            this.contexts[context_num].strokeStyle = color;
            this.contexts[context_num].strokeRect(x_pos, y_pos, this.zoomed_column, glyph_height);
          } else {
            this.contexts[context_num].fillStyle = color;
            this.contexts[context_num].fillRect(x_pos, y_pos, this.zoomed_column, glyph_height);
          }

          previous_height = previous_height + glyph_height;
        }
      }
    }


    if (this.zoom < 0.2) {
      mod = 20;
    } else if (this.zoom < 0.3) {
      mod = 10;
    }

    if(this.options.positionMarker){
      if (i % mod === 0) {
        // draw column dividers
        if(this.options.show_probs){
          draw_ticks(this.contexts[context_num], x + this.zoomed_column, this.height - 30, parseFloat(this.height), '#dddddd');
        }
        // draw top ticks
        draw_ticks(this.contexts[context_num], x + this.zoomed_column, 0, 5);

        // if ali_coordinates exist and toggle is set then display the
        // alignment coordinates and not the model coordinates.
        if (this.display_ali_map) {
          column_label = this.data.ali_map[i - 1];
        } else {
          column_label = column_num;
        }
        // draw column numbers
        draw_column_number(this.contexts[context_num], x - 2,  10, this.zoomed_column, column_label, 10, true);
      }

    }


    // draw insert probabilities/lengths
    if(this.options.show_probs){
      draw_small_insert(
        this.contexts[context_num],
        x,
        this.height - 42,
        this.zoomed_column,
        this.data.insert_probs[i - 1],
        this.data.insert_lengths[i - 1],
        this.data.delete_probs[i - 1],
        this.show_inserts
      );
    }

    if(this.options.show_probs){
      // draw other dividers
      if (this.show_inserts) {
        draw_border(this.contexts[context_num], this.height - 45, this.total_width);
      } else {
        draw_border(this.contexts[context_num], this.height - 15, this.total_width);
      }
    }

    if(this.options.border){
      draw_border(this.contexts[context_num], 0, this.total_width);
    }

    x += this.zoomed_column;
    column_num++;
  }

};


function draw_small_insert(context, x, y, col_width, in_odds, in_length, del_odds, show_inserts) {
  var fill = "#ffffff";
  if (show_inserts) {
    if (in_odds > 0.1) {
      fill = '#d7301f';
    } else if (in_odds > 0.05) {
      fill = '#fc8d59';
    } else if (in_odds > 0.03) {
      fill = '#fdcc8a';
    }
    context.fillStyle = fill;
    context.fillRect(x, y + 15, col_width, 10);

    fill = "#ffffff";
    // draw insert length
    if (in_length > 9) {
      fill = '#d7301f';
    } else if (in_length > 7) {
      fill = '#fc8d59';
    } else if (in_length > 4) {
      fill = '#fdcc8a';
    }
    context.fillStyle = fill;
    context.fillRect(x, y + 30, col_width, 10);
  } else {
    y  = y + 30;
  }

  fill = "#ffffff";
  // draw delete odds
  if (del_odds < 0.75) {
    fill = '#2171b5';
  } else if (del_odds < 0.85) {
    fill = '#6baed6';
  } else if (del_odds < 0.95) {
    fill = '#bdd7e7';
  }
  context.fillStyle = fill;
  context.fillRect(x, y, col_width, 10);
}


