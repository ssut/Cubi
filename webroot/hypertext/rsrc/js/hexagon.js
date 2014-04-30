(function() {
  "use strict";
  var hex;

  $.fn.extend({
    grandpa: function() {
      return $(this).parent().parent();
    }
  });

  hex = function() {};

  hex.ctx = (function() {
    function ctx() {
      this.storage = {};
      this.workers = {};
    }

    ctx.prototype.set = function(key, value) {
      return hex.ctx.storage[key] = value;
    };

    ctx.prototype.get = function(key) {
      return hex.ctx.storage[key];
    };

    ctx.prototype.add = function(name, fx) {
      hex.ctx.workers[name] = fx;
      return hex[name] = function() {
        return hex.call(name, arguments);
      };
    };

    ctx.prototype.invoke = function(name) {
      return hex.ctx.workers[name];
    };

    return ctx;

  })();

  hex.ctx = new hex.ctx();

  hex.set = hex.ctx.set;

  hex.get = hex.ctx.get;

  hex.add = hex.ctx.add;

  hex.call = function(name, args) {
    return hex.ctx.invoke(name)(args);
  };

  window.hex = hex;

  window.def = hex.add;

  window.glob = function(fx) {
    return $(document).ready(fx);
  };

  def('type', function(args) {
    var object, target;
    target = args[0];
    object = args[1];
    if (object) {
      if ((hex.type(target)) === object.name) {
        return true;
      } else {
        return false;
      }
    } else {
      if (target === null) {
        return 'Null';
      } else if (target === void 0) {
        return 'Undefined';
      } else if (!target.constructor.name) {
        return target.constructor.constructor.name;
      } else {
        return target.constructor.name;
      }
    }
  });

}).call(this);
