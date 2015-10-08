module.exports = function draw_column_number(context, x, y, col_width, col_num, fontsize, right) {
  context.font = fontsize + "px Arial";
  context.textAlign = right ? "right" : "center";
  context.fillStyle = "#666666";
  context.fillText(col_num, x + (col_width / 2), y);
}
