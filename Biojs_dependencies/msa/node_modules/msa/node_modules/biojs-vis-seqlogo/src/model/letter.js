module.exports = function Letter(letter, options) {
  options = options || {};
  this.value = letter;
  this.width = parseInt(options.width, 10) || 100;

  //W is 30% wider than the other letters, so need to make sure
  //it gets modified accordingly.
  if (this.value === 'W') {
    this.width += (this.width * 30) / 100;
  }

  this.height = parseInt(options.height, 10) || 100;

  this.color = options.color || '#000000';
  // if the height and width are changed from the default, then
  // this will also need to be changed as it cant be calculated
  // dynamically.
  this.fontSize = options.fontSize || 138;

  this.scaled = function () { };

  this.draw = function (ext_ctx, target_height, target_width, x, y, color) {
    var h_ratio = target_height / this.height,
    w_ratio = target_width / this.width,
    prev_font = ext_ctx.font;
    ext_ctx.transform(w_ratio, 0, 0, h_ratio, x, y);
    ext_ctx.fillStyle = color || this.color;
    ext_ctx.textAlign = "center";
    ext_ctx.font = "bold " + this.fontSize + "px Arial";

    ext_ctx.fillText(this.value, 0, 0);
    //restore the canvas settings
    ext_ctx.setTransform(1, 0, 0, 1, 0, 0);
    ext_ctx.fillStyle = '#000000';
    ext_ctx.font = prev_font;
  };

}
