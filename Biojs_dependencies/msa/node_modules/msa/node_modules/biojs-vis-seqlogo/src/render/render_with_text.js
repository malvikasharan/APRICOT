var draw_border = require("./draw/border.js");
var draw_ticks = require("./draw/ticks.js");
var draw_column_number = require("./draw/column_number.js");

module.exports = function (start, end, context_num, fontsize) {
  var x = 0,
  column_num = start,
  column_label = null,
  i = 0,
  top_height = Math.abs(this.data.max_height),
  bottom_height = (isNaN(this.data.min_height_obs)) ? 0 : parseInt(this.data.min_height_obs, 10),
  total_height = top_height + Math.abs(bottom_height),
  top_percentage    = Math.round((Math.abs(this.data.max_height) * 100) / total_height),
  //convert % to pixels
  top_pix_height = Math.round((this.info_content_height * top_percentage) / 100),
  bottom_pix_height = this.info_content_height - top_pix_height,
  // this is used to transform the 256px high letters into the correct size
  // when displaying negative values, so that they fit above the 0 line.
  top_pix_conversion = top_pix_height / this.info_content_height,
  bottom_pix_conversion = bottom_pix_height / this.info_content_height;

  // add 3 extra columns so that numbers don't get clipped at the end of a canvas
  // that ends before a large column. DF0000830 was suffering at zoom level 0.6,
  // column 2215. This adds a little extra overhead, but is the easiest fix for now.
  if (end + 3 <= this.end) {
    end += 3;
  }

  for (i = start; i <= end; i++) {
    if (this.data.mmline && this.data.mmline[i - 1] === 1) {
      this.contexts[context_num].fillStyle = '#cccccc';
      this.contexts[context_num].fillRect(x, 10, this.zoomed_column, this.height - 40);
    } else {
      var column = this.data.heightArr[i - 1],
      col_positions = [];
      if (column) {
        var previous_height = 0,
        letters = column.length,
        previous_neg_height = top_pix_height,
        j = 0,
        color = null;

        for(var j in column){
          var letter = column[j],
          values = [j,letter];
          x_pos = x + (this.zoomed_column / 2),
          letter_height = null;

          // we don't render anything with a value between 0 and 0.01. These
          // letters would be too small to be meaningful on any scale, so we
          // just squash them out.
          if (values[1] > 0.01) {
            letter_height = parseFloat(values[1]) / this.data.max_height;
            var y_pos = (this.info_content_height - 2) - previous_height,
            glyph_height = (this.info_content_height - 2) * letter_height;

            col_positions[j] = [glyph_height, this.zoomed_column, x_pos, y_pos];
            previous_height = previous_height + glyph_height;
          }
        }

        // render the letters in reverse order so that the larger letters on the top
        // don't clobber the smaller letters below them.
        //for (j = letters; j >= 0; j--) {
        for(var j in column){
          if (col_positions[j] && this.letters[j]) {

            if(this.colorscheme === 'dynamic'){
              color = this.colors.getColor(j, {pos: i - 1} );
            }else{
              if (this.colorscheme === 'consensus') {
                color = this.cmap[i - 1][j] || "#7a7a7a";
              } else {
                color = null;
              }
            }
            this.letters[j].draw(this.contexts[context_num], col_positions[j][0], col_positions[j][1], col_positions[j][2], col_positions[j][3], color);
          }
        }
      }
    }


    // if ali_coordinates exist and toggle is set then display the
    // alignment coordinates and not the model coordinates.
    if (this.display_ali_map) {
      column_label = this.data.ali_map[i - 1];
    } else {
      column_label = column_num;
    }

    if(this.options.show_divider){
      if (this.zoom < 0.7) {
        if (i % this.options.divider_step === 0) {
          draw_column_divider(this,{
            context_num : context_num,
            x : x,
            fontsize: 10,
            column_num: column_label,
            ralign: true
          });
        }
      } else {
        draw_column_divider(this,{
          context_num : context_num,
          x : x,
          fontsize: fontsize,
          column_num: column_label
        });
      }
    }

    if(this.options.show_probs){
      draw_delete_odds(this.contexts[context_num], x, this.height, this.zoomed_column, this.data.delete_probs[i - 1], fontsize, this.show_inserts);
      //draw insert length ticks
      draw_ticks(this.contexts[context_num], x, this.height - 15, 5);
      if (this.show_inserts) {
        draw_insert_odds(this.contexts[context_num], x, this.height, this.zoomed_column, this.data.insert_probs[i - 1], fontsize);
        draw_insert_length(this.contexts[context_num], x, this.height - 5, this.zoomed_column, this.data.insert_lengths[i - 1], fontsize);

        // draw delete probability ticks
        draw_ticks(this.contexts[context_num], x, this.height - 45, 5);
        // draw insert probability ticks
        draw_ticks(this.contexts[context_num], x, this.height - 30, 5);
      }

    }

    x += this.zoomed_column;
    column_num++;
  }


  if(this.options.show_probs){
    // draw other dividers
    if (this.show_inserts) {
      draw_border(this.contexts[context_num], this.height - 30, this.total_width);
      draw_border(this.contexts[context_num], this.height - 45, this.total_width);
    }
    draw_border(this.contexts[context_num], this.height - 15, this.total_width);
  }
  if(this.options.border){
    draw_border(this.contexts[context_num], 0, this.total_width);
  }
};


function draw_delete_odds(context, x, height, col_width, text, fontsize, show_inserts) {
  var y        = height - 4,
  fill     = '#ffffff',
  textfill = '#555555';

  if (show_inserts) {
    y = height - 35;
  }

  if (text < 0.75) {
    fill     = '#2171b5';
    textfill = '#ffffff';
  } else if (text < 0.85) {
    fill = '#6baed6';
  } else if (text < 0.95) {
    fill = '#bdd7e7';
  }

  draw_rect_with_text(context, x, y, text, fontsize, col_width, fill, textfill);
}

function draw_rect_with_text(context, x, y, text, fontsize, col_width, fill, textfill) {
  context.font = fontsize + "px Arial";
  context.fillStyle = fill;
  context.fillRect(x, y - 10, col_width, 14);
  context.textAlign = "center";
  context.fillStyle = textfill;
  context.fillText(text, x + (col_width / 2), y);
}

function draw_column_divider(inst, opts) {
  var div_x = opts.ralign ? opts.x + inst.zoomed_column : opts.x,
  num_x = opts.ralign ? opts.x + 2 : opts.x;
  // draw column dividers
  draw_ticks(inst.contexts[opts.context_num], div_x, inst.height - 30, -30 - inst.height, '#dddddd');
  // draw top ticks
  draw_ticks(inst.contexts[opts.context_num], div_x, 0, 5);
  // draw column numbers
  draw_column_number(inst.contexts[opts.context_num], num_x, 10, inst.zoomed_column, opts.column_num, opts.fontsize, opts.ralign);
};



function draw_insert_odds(context, x, height, col_width, text, fontsize) {
  var y        = height - 20,
  fill     = '#ffffff',
  textfill = '#555555';

  if (text > 0.1) {
    fill     = '#d7301f';
    textfill = '#ffffff';
  } else if (text > 0.05) {
    fill = '#fc8d59';
  } else if (text > 0.03) {
    fill = '#fdcc8a';
  }

  draw_rect_with_text(context, x, y, text, fontsize, col_width, fill, textfill);

  //draw vertical line to indicate where the insert would occur
  if (text > 0.03) {
    draw_ticks(context, x + col_width, height - 30, -30 - height, fill);
  }
}
function draw_insert_length(context, x, y, col_width, text, fontsize) {
  var fill = '#ffffff',
  textfill = '#555555';

  if (text > 9) {
    fill     = '#d7301f';
    textfill = '#ffffff';
  } else if (text > 7) {
    fill = '#fc8d59';
  } else if (text > 4) {
    fill = '#fdcc8a';
  }
  draw_rect_with_text(context, x, y, text, fontsize, col_width, fill, textfill);
}
