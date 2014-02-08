$(document).ready(function() {
	'use strict';

	Cubi.registerEvent('registerNext', function() {
		if(parseInt($('body > section.blind section#Register section:first-child h1 span:first-child').html()) <= 3) {
			$('body > section.blind section#Register section:first-child').animate({
				left: parseInt($('body > section.blind section#Register section:first-child').css('left')) + 45
			}, 500);

			$('body > section.blind section#Register section:first-child h1 span:first-child').html(parseInt($('body > section.blind section#Register section:first-child h1 span:first-child').html()) + 1);

			setTimeout(function() {
				$('body > section.blind section#Register section:first-child > input[type=button]').eq(0).removeAttr('disabled');
			}, 500)
		}
	});

	Cubi.registerEvent('registerNext1', function() {
		$('body > section.blind section#Register section:first-child h1 span:nth-child(2)').html('개인정보취급방침');
		$('body > section.blind section#Register section:first-child > section textarea').html('개인정보취급방침 내용');
		$('body > section.blind section#Register section:first-child > input[type=button]').eq(0).val('개인정보취급방침에 동의');
	});

	Cubi.registerEvent('registerNext2', function() {
		$('body > section.blind section#Register section:first-child h1 span:nth-child(2)').html('개인 정보 입력');
		$('body > section.blind section#Register section:first-child > section').html('');
		
		Cubi.loadContent('static/tpl/register.form.tpl', {
			additionalRsrc: ['static/css/register.form.css'],
			instantlyMode: true,
			instantTarget: 'body > section.blind section#Register section:first-child > section'
		});

		$('body > section.blind section#Register section:first-child > input[type=button]').eq(0).val('입력 완료');
	});

	Cubi.registerEvent('registerNext3', function() {
		$('body > section.blind section#Register section:first-child h1 span:nth-child(2)').html('회원 가입 완료');
		$('body > section.blind section#Register section:first-child > section').html('<h2>가입이 완료되었습니다!</h2>');
		$('body > section.blind section#Register section:first-child > input[type=button]').eq(1).hide();
		$('body > section.blind section#Register section:first-child > input[type=button]').eq(0).val('닫기').click(function() {
			$('body > section.blind section#Register').animate({
				top: -500
			}, 1000);

			$('body > section.blind section#Register').parent().fadeOut('slow', function() {
				$(this).remove();
			});
		});
	});

	Cubi.registerEvent('registerPageLoad', function() {
		$('body > section.blind section#Register').parent().fadeIn();
		$('body > section.blind section#Register section:first-child > input[type=button]').eq(0).click(function() {
			$(this).attr('disabled', 'disabled');

			if(parseInt($('body > section.blind section#Register section:first-child h1 span:first-child').html()) == 3) {
				var registerStatus = false;
				$.ajax({
					url: "/user/new",
					type: "POST",
					data: {
						email: $('#registerEmail').val(),
						nick: $('#registerNick').val(),
						pw: $('#registerPw').val()
					},
					success: function(response) {

					}
				});
				
				if(registerStatus) {
					Cubi.invokeEvent('registerNext' + parseInt($('body > section.blind section#Register section:first-child h1 span:first-child').html()));
					Cubi.invokeEvent('registerNext');
				} else {
					$('body > section.blind section#Register section:first-child > input[type=button]').eq(0).removeAttr('disabled');
				}

				 
			} else {
				Cubi.invokeEvent('registerNext' + parseInt($('body > section.blind section#Register section:first-child h1 span:first-child').html()));
				Cubi.invokeEvent('registerNext');
			}
		});

		$('body > section.blind section#Register section:first-child > input[type=button]').eq(1).click(function() {
			$('body > section.blind section#Register').animate({
				top: -500
			}, 1000);

			$('body > section.blind section#Register').parent().fadeOut('slow', function() {
				$('body > section.blind section#Register').parent().remove();
			});
		});
	});
});