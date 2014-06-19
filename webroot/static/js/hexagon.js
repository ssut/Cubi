(function() {
  "use strict";
  var hex;

  $.fn.extend({
    grandpa: function() {
      return $(this).parent().parent();
    }
  });

  $.fn.extend({
    child: function(selector) {
      return $(this).children(selector);
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

  hex.env = (function() {
    var UA, Version, isAndroid, isApple, isChrome, isExplorer, isFirefox, isMacintosh, isMobile, isOpera, isSafari, isWebkit, isWindows, uaCheck;
    uaCheck = function(regularExpression) {
      return (new RegExp(regularExpression)).test(navigator.userAgent);
    };
    Version = 0;
    UA = navigator.userAgent;
    isSafari = uaCheck('WebKit') && uaCheck('Safari') && !uaCheck('Chrome') && !uaCheck('OPR');
    isChrome = uaCheck('WebKit') && uaCheck('Safari') && uaCheck('Chrome') && !uaCheck('OPR');
    isFirefox = uaCheck('Firefox');
    isExplorer = uaCheck('MSIE');
    isOpera = uaCheck('Opera') && !uaCheck('WebKit') || uaCheck('WebKit') && uaCheck('Safari') && uaCheck('Chrome') && uaCheck('OPR');
    isWebkit = uaCheck('WebKit');
    isMobile = uaCheck('Mobile');
    isAndroid = uaCheck('Android');
    isApple = uaCheck('iP(hone|ad|od)');
    isWindows = uaCheck('Windows');
    isMacintosh = uaCheck('Macintosh');
    if (isSafari || isOpera && !isWebkit) {
      Version = (new RegExp('\s*Version\/([0-9\.]+)\s*')).exec(UA)[0].trim().split('/')[1];
    } else if (isChrome) {
      Version = (new RegExp('\s*Chrome\/([0-9\.]+)\s*')).exec(UA)[0].trim().split('/')[1];
    } else if (isFirefox) {
      Version = (new RegExp('\s*Firefox\/([0-9\.]+)\s*')).exec(UA)[0].trim().split('/')[1];
    } else if (isExplorer) {
      Version = /\s*MSIE\s+([0-9\.]+)\s*/.exec(UA)[1];
    } else if (isOpera && isWebkit) {
      Version = (new RegExp('\s*OPR\/([0-9\.]+)\s*')).exec(UA)[0].trim().split('/')[1];
    }
    Version = Version.split('.');
    Version = parseFloat(Version.shift() + '.' + Version.join(''));
    return {
      agent: isSafari ? 'safari' : (isChrome ? 'chrome' : (isFirefox ? 'firefox' : (isExplorer ? 'ie' : (isOpera ? 'opera' : 'unknown')))),
      ver: Version,
      os: isMobile ? (isAndroid ? 'android' : (isApple ? 'ios' : 'mobile')) : (isWindows ? 'windows' : (isMacintosh ? 'macintosh' : 'unknown'))
    };
  })();

  window.hex = hex;

  window.def = hex.add;

  window.glob = function(fx) {
    return $(document).ready(fx);
  };

  window.declare = function(code) {
    return code();
  };

  window.run = function(name, period) {
    return setInterval((function() {
      return hex.call(name);
    }), period);
  };

  glob(function() {
    $('html').attr('agent', hex.env.agent);
    $('html').attr('version', hex.env.ver);
    $('html').attr('os', hex.env.os);
    if (hex.env.agent !== 'ie') {
      return $('html').attr('noie', 'noie');
    }
  });

  def('define', function(args) {
    var key, value;
    key = args[0];
    value = args[1];
    return window['_' + key] = value;
  });

  def('switch', function(args) {
    var item;
    item = args[0];
    return hex.set(item, !(hex.get(item)));
  });

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
