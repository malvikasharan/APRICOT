var ArrayProto = Array.prototype;
var slice = ArrayProto.slice;

var _ = {};

// Determines whether to execute a function as a constructor
// or a normal function with the provided arguments
var executeBound = function(sourceFunc, boundFunc, context, callingContext, args) {
  if (!(callingContext instanceof boundFunc)) return sourceFunc.apply(context, args);
  var self = baseCreate(sourceFunc.prototype);
  var result = sourceFunc.apply(self, args);
  if (_.isObject(result)) return result;
  return self;
};

// Partially apply a function by creating a version that has had some of its
// arguments pre-filled, without changing its dynamic `this` context. _ acts
// as a placeholder, allowing any combination of arguments to be pre-filled.
var partial = function(func) {
  var boundArgs = slice.call(arguments, 1);
  return function bound() {
    var position = 0;
    var args = boundArgs.slice();
    for (var i = 0, length = args.length; i < length; i++) {
      if (args[i] === _) args[i] = arguments[position++];
    }
    while (position < arguments.length) args.push(arguments[position++]);
    return executeBound(func, bound, this, this, args);
  };
};

// Delays a function for the given number of milliseconds, and then calls
// it with the arguments supplied.
var delay = function(func, wait) {
  var args = slice.call(arguments, 2);
  return setTimeout(function() {
    return func.apply(null, args);
  }, wait);
};

// Defers a function, scheduling it to run after the current call stack has
// cleared.
var defer = partial(delay, _, 1);
module.exports = defer;
