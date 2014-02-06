$(document).ready(function() {
	'use strict';

	Cubi.registerEvent('signInClose', function() {
		$('body > section.blind section#signIn').animate({
			top: -500
		}, 1000);

		$('body > section.blind section#signIn').parent().fadeOut('slow', function() {
			$(this).remove();
		});
	});

	Cubi.registerEvent('signInPageLoad', function() {
		$('body > section.blind section#signIn').parent().fadeIn();

		$('body > section.blind section#signIn > section input:first-child').click(function() {
			if($(this).val() == '로그인') {
				/**

				 if(로그인 성공 여부) {
					 location.reload();
				 } else {
					 alert(로그인 실패 메시지 출력);
				 }

				 **/
			} else if($(this).val() == '비밀번호 재발급 이메일 보내기') {
				/**

				 알아서 뭘로든 보내면 됨ㅋ

				 **/

				alert('재발급 메일을 보냈습니다.\n약간의 시간 후 메일을 확인하시기 바랍니다.');

				Cubi.invokeEvent('signInClose');
			}
		});

		$('body > section.blind section#signIn > section input:nth-child(2)').click(function() {
			$('body > section.blind section#signIn').parent().fadeOut('fast', function() {
				$(this).remove();

				Cubi.invokeEvent('userRegister');
			});
		});

		$('body > section.blind section#signIn > section input:nth-child(3)').click(function() {
			$('body > section.blind section#signIn h1 span').html('비밀번호 찾기');
			$('body > section.blind section#signIn > section input').hide();
			$('body > section.blind section#signIn > section input:first-child').val('비밀번호 재발급 이메일 보내기').show();
			$('body > section.blind section#signIn > input:nth-child(3)').attr('placeholder', '닉네임');
			$('body > section.blind section#signIn > input').each(function() {
				$(this).val('');
			});
		});
	});
});