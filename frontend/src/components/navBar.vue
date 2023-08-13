<template>
    <nav class="navbar navbar-expand-lg navbar-light p-0" style="background-color: #E4F0AF">
  <div class="container-fluid">
	<a href="/admin_dashboard" v-if="this.loggedin && this.isadmin" class="navbar-brand"><h4>Admin Dashboard</h4></a>
	<a href="/shows" v-else-if="this.loggedin && ! this.isadmin" class="navbar-brand"><h4>User Dashboard</h4></a>
	<a href="/shows" v-else class="navbar-brand"><h4>Very Good Ticket Booking Site</h4></a>
	<div class="d-flex flex-row-reverse">
		<div class="collapse navbar-collapse col-4 " id="navbarSupportedContent">
			<ul class="navbar-nav">
                <li v-if="this.loggedin" class="nav-item">
                    <h4 class="navbar-brand">Welcome {{ username }}!</h4>
                </li>
				<li v-if="! this.loggedin" class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to="/login"
                        >Login 
                    </router-link>
                </li>
                <li v-if="! this.loggedin" class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to=/register
                        >Register 
                    </router-link>
                </li>
                <li v-if="this.isadmin" class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to=/admin_dashboard
                        >Admin Dashboard 
                    </router-link>
                </li>
                <li v-if="this.isadmin" class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to=/summary
                        >Admin Summary 
                    </router-link>
                </li>
                <li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to=/shows
                        >Shows 
                    </router-link>
                </li>
                <li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to=/search
                        >Search 
                    </router-link>
                </li>
                <li v-if="this.loggedin && ! this.isadmin" class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        to=/bookings
                        >Bookings
                    </router-link>
                </li>
                <li v-if="this.loggedin" class="nav-item p-2">
                    <button
                        class="btn btn-success nav-item"
                        @click="logOut"
                        >Logout
                    </button>
                </li>
			</ul>
		</div>
	</div>
  </div>
</nav>
</template>

<script>
import axios from 'axios'
export default {
    name: "Navbar",
    data(){
        return{
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            username:'',
            isadmin:false,
            loggedin:false
        }
    },
    methods:{
        async isLoggedin(){
            if(this.userSession != null){this.loggedin=true}
        },
        async logOut(){
            if(this.loggedin){
                localStorage.removeItem("userSession")
                location.href="/login"
            }
            else{console.log("Ducking user not logged in.")}
        },
        async getUsername(){
            if (this.userSession){
					axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
            await axios
                .get("http://127.0.0.1:8090/api/username")
                .then((response)=>response)
                .then((response)=>response.data)
                .then((response)=>{this.username=response})
            }else{
                console.log('getusername ERROR')
            }
        },
        async isAdmin(){
				if (this.userSession){
					axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;

				await axios
					.get('http://127.0.0.1:8090/api/isadmin')
					.then((response)=>response)
					.then((response)=>response.data)
					.then((response)=>{this.isadmin=response[0]})
                }else{console.log('User Not Loggedin')}
		}
    },
    async beforeMount(){
        this.isAdmin();
        this.isLoggedin();
        this.getUsername();
    }
}
</script>
