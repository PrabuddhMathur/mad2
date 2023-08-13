<template>
    <div class="container mv-8">
			<div class="row justify-content-center">
				<div class="card col-8">
					<div class="card-body">
						<form @submit.prevent="registerUser">
							<h3 class="card-title text-center">User Registeration</h3>
							<div class="form-floating mb-3">
								<input class="form-control" id="floatingInput" type="email" placeholder="name@example.com" name="email" v-model="email" required>
								<label for="floatingInput">Email</label>
							</div>
							<div class="form-floating mb-3">
								<input id="floatingUsername" class="form-control" type="text" placeholder="Username" name="username" v-model="username" required>
								<label for="floatingUsername">Username</label>
							</div>
							<div class="form-floating mb-3">
								<input id="floatingPassword" class="form-control" type="password" placeholder="Password" name="password" v-model="password" required>
								<label for="floatingPassword">Password</label>
							</div>
							<div class="form-floating mb-3">
								<input id="floatingpassword_confirm" class="form-control" type="password" placeholder="password_confirm" name="password_confirm" v-model="password2" required>
								<label for="floatingpassword_confirm">Re-Enter Password</label>
							</div>
							<div class="row justify-content-center text-end m-2">
								<div class="col"><a href="/login">Click here for User Login</a></div>
							</div>
							<div class="row justify-content-center text-center">
								<div class="col"><button class="btn btn-success" value="Register" name="submit" type="submit">Register</button></div>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
</template>
<script>
import axios from 'axios';
export default {
	name:"RegisterView",
	data(){
		return {
			userSession: JSON.parse(localStorage.getItem("userSession")) || null,
			email:"",
			username:"",
			password:"",
			password2:"",
			token:"",
			expiry:""
		}
	},
	methods:{
		async registerUser(){
			if (this.password===this.password2){
				await axios
					.post("http://127.0.0.1:8090/api/register",{
						email: this.email,
						username: this.username,
						password: this.password
					})
					.then((response) => response["data"])
					.then((response)=>{return response;})
					.then((response) => (
					(this.token = response.token), (this.expiry = response.exp)
					))
					this.userSession = {
					token: this.token,
					expiry: this.expiry,
					};
					localStorage.setItem("userSession", JSON.stringify(this.userSession));
					location.href="/admin_dashboard"
					
			}
		}
	}
}
</script>