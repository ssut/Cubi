<section class="blind">
	<section id="signIn">
		<h1>
			<span>로그인</span>
			<a href="javascript:Cubi.invokeEvent('signInClose')">
				<img src="static/img/btn.signin.png" alt="닫기">
			</a>
		</h1>
		<input type="text" id="signInEmail" placeholder="이메일">
		<input type="password" id="signInPw" placeholder="비밀번호">
		<section>
			<input type="button" value="로그인">
			<input type="button" value="회원 가입">
			<input type="button" value="비밀번호 찾기">
		</section>
	</section>
</section>
<script>
	Cubi.invokeEvent('signInPageLoad');
</script>