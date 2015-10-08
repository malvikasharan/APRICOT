module.exports = function draw_border(context, y, width) {
  context.beginPath();
  context.moveTo(0, y);
  context.lineTo(width, y);
  context.lineWidth = 1;
  context.strokeStyle = "#999999";
  context.stroke();
}
