module.exports = function draw_ticks(context, x, y, height, color) {
  color = color || '#999999';
  context.beginPath();
  context.moveTo(x, y);
  context.lineTo(x, y + height);
  context.lineWidth = 1;
  context.strokeStyle = color;
  context.stroke();
}
