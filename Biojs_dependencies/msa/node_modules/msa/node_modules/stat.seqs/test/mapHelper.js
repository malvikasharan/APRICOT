var _ = require("underscore");
var map = {};
map.roundArr = function round(arr, to) {
  return arr.map(function(el) {
    return parseFloat(+el.toFixed(to || 2));
  });
};

map.roundMap = function roundMap(arr, to) {
  return _.each(arr, function(val, key, obj) {
    obj[key] = parseFloat(+val.toFixed(to || 2));
  });
};

map.roundArrMap = function roundArrMap(arr, to) {
  return _.map(arr, function(e) {
    return map.roundMap(e, to);
  });
};

map.roundMapMap = function roundMapMap(arr, to) {
  return _.each(arr, function(val, key, obj) {
    obj[key] = val = map.roundMap(val, to);
    return val;
  });
};

module.exports = map;
