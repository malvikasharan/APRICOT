var koalajs = {};

// pass an alternative default value
koalajs.d = koalajs.defaultValue = function defaultValue(obj, defValue) {
  if (obj === undefined) {
    if (typeof obj === "function") {
      return defValue();
    }
    return defValue;
  }
  return obj;
};

// alias for getElementById
koalajs.id = function mk(el) {
  return document.getElementById(el);
};

// alias for createElement
koalajs.mk = function mk(el) {
  return document.createElement(el);
};

if (module !== undefined && module.exports !== undefined) {
  module.exports = koalajs;
}
