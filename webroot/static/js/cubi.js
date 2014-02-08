$(document).ready(function() {
	'use strict';

	// Cubi framework
	var Cubi = new function() {
		var Events = {}, Resources = {};

		this.registerEvent = function(eventName, eventCtx) {
			if(!Events[eventName]) {
				Events[eventName] = eventCtx;
			}
		};

		this.invokeEvent = function(eventName, eventArgs) {
			if(Events[eventName]) {
				(function(eventCtx, Args) {
					eventCtx(Args);
				})(Events[eventName], eventArgs);
			}
		};

		this.loadResource = function(resourceUrl) {
			if(!Resources[resourceUrl]) {
				if((new RegExp('\.js$')).test(resourceUrl)) {
					$('head').append('<script src="' + resourceUrl + '"></script>');

					Resources[resourceUrl] = true;
				} else if((new RegExp('\.css$')).test(resourceUrl)) {
					$('head').append('<link rel="stylesheet" href="' + resourceUrl + '">');

					Resources[resourceUrl] = true;
				}
			}
		};

		this.loadContent = function(dataUrl, Options) {
			var handlingResult = null, afterHandler = function(gainData, Options) {
				if(gainData && Options) {
					if(Options.additionalRsrc) {
						for(var Index = 0; Index < Options.additionalRsrc.length; Index++) {
							Cubi.loadResource(Options.additionalRsrc[Index]);
						}
					}

					if(Options.instantlyMode) {
						if(Options.instantTarget) {
							$(Options.instantTarget).append(gainData);
						} else {
							$('body').append(gainData);
						}

						return true;
					} else {
						return gainData;
					}
				} else {
					return false;
				}
			};

			$.ajax({
				type: 'get',
				url: dataUrl,
				success: function(responseData) {
					handlingResult = afterHandler(responseData, Options);
				}
			});

			return handlingResult;
		};
	};

	window.Cubi = Cubi;

	// After processing
	Cubi.registerEvent('goTop', function() {
		document.documentElement.scrollTop = 0;
	});

	Cubi.registerEvent('userRegister', function() {
		Cubi.loadContent('static/tpl/register.tpl', {
			additionalRsrc: [
				'static/js/register.js',
				'static/css/register.css',
				'static/css/form.css'
			],
			instantlyMode: true
		});
	});

	Cubi.registerEvent('userSignIn', function() {
		Cubi.loadContent('static/tpl/signin.tpl', {
			additionalRsrc: [
				'static/js/signin.js',
				'static/css/signin.css',
				'static/css/form.css'
			],
			instantlyMode: true
		});
	});

	if($(document).height() > $('html').get(0).scrollHeight) {
		$('footer').css({
			position: 'fixed',
			bottom: 0,
			right: 0,
			left: 0
		});
	}
});