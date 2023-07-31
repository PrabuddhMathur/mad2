<template>
    <body>
		<div class="container mv-8">
			<div class="row justify-content-center">
			<form action="{{ url_for('security.login') }}" name="login_user_form" method="POST">
				<div class="card col-8">
					<div class="card-body">
						<h3 class="card-title text-center">Login</h3>
						<div class="form-floating mb-3">
							<input class="form-control" id="floatingInput" type="text" required placeholder="name@example.com" name="email">
							<label for="floatingInput">Email</label>
						</div>
						<div class="form-floating mb-3">
							<input id="password" class="form-control" type="password" placeholder="Password" name="password">
							<label for="password">Password</label>
						</div>
						<!-- <div class="form-floating mb-3">
							<label for="remember">Remember Me</label> <input id="remember" name="remember" type="checkbox" value="y">
							
						</div> -->
						<!-- <p><input id="next" name="next" type="hidden" value=""></p> -->
						<div class="row justify-content-center text-center">
							<div class="col"><input class="btn btn-success" id="submit" name="submit" value="Login" type="submit"></div>
							<div class="col"><a href="{{ url_for('security.register') }}" class="btn btn-primary" type="button">Register</a></div>
							<!-- <div class="col"><a href="{{ url_for('admin_login') }}" class="btn btn-primary" type="button">Click here for Admin Login</a></div> -->
						</div>
					</div>
				</div>
			</form>
			</div>
		</div>
   	</body>
</template>

<script>
</script>