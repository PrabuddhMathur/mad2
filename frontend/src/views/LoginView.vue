<template>
    <!-- <body> -->
		<div class="container mv-8">
			<div class="row justify-content-center">
				<div class="card col-8">
					<div class="card-body">
						<form @submit.prevent="logIn">
							<h3 class="card-title text-center">Login</h3>
							<div class="form-floating mb-3">
								<input class="form-control" id="floatingInput" type="email" required placeholder="name@example.com" name="email" v-model="email">
								<label for="floatingInput">Email</label>
							</div>
							<div class="form-floating mb-3">
								<input id="password" class="form-control" type="password" required placeholder="Password" name="password" v-model="password">
								<label for="password">Password</label>
							</div>
							
							<div class="row justify-content-center text-center">
								<div class="col"><button class="btn btn-success" type="submit">Login</button></div>
								<div class="col"><router-link class="btn btn-primary" type="button" :to="register">Register</router-link></div>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
   	<!-- </body> -->
</template>

<script>
import axios from 'axios';
export default {
	name:"LoginView",
	data(){
		return {
			userSession: JSON.parse(localStorage.getItem("userSession")) || null,
			email:"",
			password:"",
		}
	},
	methods:{
		async logIn(){
			await axios
				.post("http://127.0.0.1:8090/api/login",{
					email:this.email,
					password:this.password
				})
				.then((response)=>response)
				.then((response)=>response.data)
				.then((response)=>{
					if ("Error" in response){
						throw response
					}
					else{return response}
				})
				.then((response) => {
				this.token = response.token
				this.expiry = response.expiry
				this.userSession = {
				token: this.token,
				expiry: this.expiry,
				};
				console.log(this.userSession)
				localStorage.setItem("userSession", JSON.stringify(this.userSession));
				location.href="/shows"
				
				})
				.catch((response)=>{
					alert(response['errorMessage'])
				})
				
				
		}
	},
	computed:{
	register() {
            return "/register"
        },
	}
}
</script>