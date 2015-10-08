module.exports = {
    render_x_axis_label: function () {
      var label = "Model Position";
      if (this.display_ali_map) {
        label = "Alignment Column";
      }
      this.called_on.find('.logo_xaxis').remove();
      this.called_on.prepend('<div class="logo_xaxis" class="centered" style="margin-left:40px"><p class="xaxis_text" style="width:10em;margin:1em auto">' + label + '</p></div>');

    },
    render_y_axis_label: function () {
      //attach a canvas for the y-axis
      this.dom_element.parent().before('<canvas class="logo_yaxis" height="'+this.options.height+'" width="55"></canvas>');
      var canvas = this.called_on.find('.logo_yaxis'),
      top_pix_height = 0,
      bottom_pix_height = 0,
      top_height = Math.abs(this.data.max_height),
      bottom_height = (isNaN(this.data.min_height_obs)) ? 0 : parseInt(this.data.min_height_obs, 10),
      context = null,
      axis_label = "Information Content (bits)";

      context = canvas[0].getContext('2d');
      //draw min/max tick marks
      context.beginPath();
      context.moveTo(55, 1);
      context.lineTo(40, 1);

      context.moveTo(55, this.info_content_height);
      context.lineTo(40, this.info_content_height);


      context.moveTo(55, (this.info_content_height / 2));
      context.lineTo(40, (this.info_content_height / 2));
      context.lineWidth = 1;
      context.strokeStyle = "#666666";
      context.stroke();

      //draw the label text
      context.fillStyle = "#666666";
      context.textAlign = "right";
      context.font = "bold 10px Arial";

      // draw the max label
      context.textBaseline = "top";
      context.fillText(parseFloat(this.data.max_height).toFixed(1), 38, 0);
      context.textBaseline = "middle";

      // draw the midpoint labels
      context.fillText(parseFloat(this.data.max_height / 2).toFixed(1), 38, (this.info_content_height / 2));
      // draw the min label
      context.fillText('0', 38, this.info_content_height);

      // draw the axis label
      if (this.data.height_calc === 'score') {
        axis_label = "Score (bits)";
      }

      context.save();
      context.translate(5, this.height / 2 - 20);
      context.rotate(-Math.PI / 2);
      context.textAlign = "center";
      context.font = "normal 12px Arial";
      context.fillText(axis_label, 1, 0);
      context.restore();

      // draw the insert row labels
      context.fillText('occupancy', 55, this.info_content_height + 7);
      if (this.show_inserts) {
        context.fillText('ins. prob.', 50, 280);
        context.fillText('ins. len.', 46, 296);
      }
    }
}; 
