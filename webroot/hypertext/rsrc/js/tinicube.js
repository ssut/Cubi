(function() {
  "use strict";
  def('animate', function(args) {
    var duration, notation, property, selector, to;
    selector = args[0];
    property = args[1];
    to = args[2];
    duration = args[3];
    notation = [{}, {}];
    notation[0][property] = to;
    notation[1] = {
      duration: duration,
      queue: false
    };
    return $(selector).animate(notation[0], notation[1]);
  });

  def('toggle', function(args) {
    var from, origin, selector, to;
    selector = args[0];
    from = args[1];
    to = args[2];
    origin = $(selector).css(from);
    hex.animate(selector, from, $(selector).css(to), 'fast');
    hex.animate(selector, to, origin, 'fast');
    return $(selector);
  });

  hex.set('promoteIndex', 0);

  def('promoteToggle', function(args) {
    var target;
    target = args[0] % 3;
    hex.set('promoteIndex', target);
    if ($('header > .p:nth-child(2) > .p nav ul li a.selected').get(0) !== $('header > .p:nth-child(2) > .p nav ul li a').eq(target).get(0)) {
      hex.toggle('header > .p:nth-child(2) > .p nav ul li a.selected', 'background-color', 'color').removeClass('selected');
      hex.toggle($('header > .p:nth-child(2) > .p nav ul li a').eq(target), 'background-color', 'color').addClass('selected');
      $('header > .p:nth-child(2) > .p > section.p.show').fadeOut('fast', function() {
        return $(this).removeClass('show').addClass('hide');
      });
      $('header > .p:nth-child(2) > .p > section.p').eq(target).fadeIn('fast', function() {
        return $(this).removeClass('hide').addClass('show');
      });
    }
    return void 0;
  });

  setInterval((function() {
    return hex.promoteToggle((hex.get('promoteIndex')) + 1);
  }), 3500);

  if (!$('body').hasClass('not-index')) {
    $(document).scroll(function() {
      return $('header > section').eq(0).css('background-color', 'rgba(52, 152, 219, ' + (0.5 + $('body').get(0).scrollTop / 990) + ')');
    });
  }

  def('searchToggle', function(args) {
    if ($('header > .p:first-child > .p section input').hasClass('hide')) {
      $('header > .p:first-child > .p section input').show().width(0).css('opacity', 0).animate({
        opacity: 1,
        width: 104
      }, 400, function() {
        $(this).parent().find('img').hide().attr('src', 'rsrc/img/icon.search.blue.png').fadeIn('fast');
        return $('header > .p:first-child > .p > section input').focus();
      }).removeClass('hide');
    }
    return void 0;
  });

  glob(function() {
    return $('header > .p:first-child > .p > section input').blur(function() {
      return $(this).animate({
        opacity: 0,
        width: 0
      }, 400, function() {
        return $(this).hide().parent().find('img').hide().attr('src', 'rsrc/img/icon.search.png').fadeIn('fast');
      }).addClass('hide');
    });
  });

  def('favoriteToggle', function(args) {
    var target;
    target = args[0];
    if (target === 1 && !$('header > .p:first-child > .p > ul > li > section nav li:nth-child(2)').hasClass('selected')) {
      (hex.animate((hex.animate((hex.animate('header > .p:first-child > .p > ul > li > section nav li:first-child', 'background-color', 'rgb(41, 128, 185)', 'fast')).find('b'), 'color', 'rgb(255, 255, 255)', 'fast')).grandpa(), 'border-bottom-color', 'rgb(41, 128, 185)', 'fast')).removeClass('selected');
      (hex.animate((hex.animate((hex.animate('header > .p:first-child > .p > ul > li > section nav li:nth-child(2)', 'background-color', 'rgb(236, 240, 241)', 'fast')).find('b'), 'color', 'rgb(52, 73, 94)', 'fast')).grandpa(), 'border-bottom-color', 'rgb(236, 240, 241)', 'fast')).addClass('selected');
      hex.animate('header > .p:first-child > .p > ul > li > section section article:first-child', 'left', '-122px');
      hex.animate('header > .p:first-child > .p > ul > li > section section article:nth-child(2)', 'left', '0');
    } else if (target === 0 && !$('header > .p:first-child > .p > ul > li > section nav li:first-child').hasClass('selected')) {
      (hex.animate((hex.animate((hex.animate('header > .p:first-child > .p > ul > li > section nav li:nth-child(2)', 'background-color', 'rgb(41, 128, 185)', 'fast')).find('b'), 'color', 'rgb(255, 255, 255)', 'fast')).grandpa(), 'border-bottom-color', 'rgb(41, 128, 185)', 'fast')).removeClass('selected');
      (hex.animate((hex.animate((hex.animate('header > .p:first-child > .p > ul > li > section nav li:first-child', 'background-color', 'rgb(236, 240, 241)', 'fast')).find('b'), 'color', 'rgb(52, 73, 94)', 'fast')).grandpa(), 'border-bottom-color', 'rgb(236, 240, 241)', 'fast')).addClass('selected');
      hex.animate('header > .p:first-child > .p > ul > li > section section article:first-child', 'left', '0');
      hex.animate('header > .p:first-child > .p > ul > li > section section article:nth-child(2)', 'left', '122px');
    }
    return void 0;
  });

  def('favoriteViewToggle', function(args) {
    if ($('header > .p:first-child > .p > ul > li > section').css('display') === 'none') {
      hex.animate($('header > .p:first-child > .p > ul > li > section').css('margin-top', -15).fadeIn('fast'), 'margin-top', '-5px', 'fast');
    } else {
      hex.animate($('header > .p:first-child > .p > ul > li > section').fadeOut('fast'), 'margin-top', '-15px', 'fast');
    }
    return void 0;
  });

  hex.set('favoriteArea', false);

  glob(function() {
    $('header > .p:first-child > .p > ul > li > section').mouseenter(function() {
      return hex.set('favoriteArea', true);
    });
    $('header > .p:first-child > .p > ul > li > section').mouseleave(function() {
      return hex.set('favoriteArea', false);
    });
    return $(document).click(function() {
      if ($('header > .p:first-child > .p > ul > li > section').css('display') === 'block' && !(hex.get('favoriteArea'))) {
        return hex.favoriteViewToggle();
      }
    });
  });

}).call(this);
