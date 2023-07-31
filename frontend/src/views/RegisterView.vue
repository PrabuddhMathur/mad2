<template>
    <div class="container mv-8">
			<div class="row justify-content-center">
			<form action="{{ url_for('security.register') }}" method="POST" onsubmit="validation();">
				<div class="card col-8">
					<div class="card-body">
						<h3 class="card-title text-center">User Registeration</h3>
						<div class="form-floating mb-3">
							<input class="form-control" id="floatingInput" type="email" placeholder="name@example.com" name="email">
							<label for="floatingInput">Email</label>
						</div>
						<div class="form-floating mb-3">
							<input id="floatingUsername" class="form-control" type="text" placeholder="Username" name="username">
							<label for="floatingUsername">Username</label>
						</div>
						<div class="form-floating mb-3">
							<input id="floatingPassword" class="form-control" type="password" placeholder="Password" name="password">
							<label for="floatingPassword">Password</label>
						</div>
						<div class="form-floating mb-3">
							<input id="floatingpassword_confirm" class="form-control" type="password" placeholder="password_confirm" name="password_confirm">
							<label for="floatingpassword_confirm">Re-Enter Password</label>
						</div>
						<div class="row justify-content-center text-end m-2">
							<div class="col"><a href="/login">Click here for User Login</a></div>
						</div>
						<div class="row justify-content-center text-center">
							<div class="col"><input class="btn btn-success" value="Register" name="submit" type="submit" ></div>
						</div>
					</div>
				</div>
			</form>
			</div>
		</div>
</template>
<script>

</script>