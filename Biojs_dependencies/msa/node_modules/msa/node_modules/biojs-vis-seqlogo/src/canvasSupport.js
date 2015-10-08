var canv_support = null;

module.exports = function canvasSupport() {
  if (!canv_support) {
    var elem = document.createElement('canvas');
    canv_support = !!(elem.getContext && elem.getContext('2d'));
  }
  return canv_support;
}
