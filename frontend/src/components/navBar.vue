<template>
    <nav class="navbar navbar-expand-lg navbar-light p-0" style="background-color: #E4F0AF">
  <div class="container-fluid">
	<a class="navbar-brand" href="/user_dashboard">User Dashboard</a>
	<div class="d-flex flex-row-reverse">
		<div class="collapse navbar-collapse col-4 " id="navbarSupportedContent">
			<ul class="navbar-nav">
				<!-- <li class="nav-item p-2"><a class="nav-item btn btn-success" href="{{ url_for('all_shows') }}">All Shows</a></li> -->
				<li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        :to="login"
                        >Login 
                    </router-link>
                </li>
                <li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        :to="register"
                        >Register 
                    </router-link>
                </li>
                <li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        :to="admin_dashboard"
                        >Admin Dashboard 
                    </router-link>
                </li>
                <li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        :to="shows"
                        >Shows 
                    </router-link>
                </li>
                <li class="nav-item p-2">
                    <router-link
                        class="btn btn-success nav-item"
                        :to="search"
                        >Search 
                    </router-link>
                </li>
				<!-- <li class="nav-item p-2"><a class="nav-item btn btn-success" href="{{ url_for('user_bookings') }}">Bookings</a></li> -->
				<!-- <li class="nav-item p-2"><a class="nav-item btn btn-success" href="#">Logout</a></li> -->
			</ul>
		</div>
	</div>
  </div>
</nav>
</template>

<script>
export default {
    name: "Navbar",
    computed: {
        login() {
            return "/login"
        },
        register() {
            return "/register"
        },
        admin_dashboard(){
            return "/admin_dashboard"
        },
        shows (){
            return "/shows"
        },
        search (){
            return "/search"
        }
    },
}
</script>
