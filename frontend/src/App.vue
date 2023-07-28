<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import HomeView from './views/HomeView.vue';
</script>

<template>
<body>
<nav class="navbar navbar-expand-lg navbar-light p-0" style="background-color: #E4F0AF">
  <div class="container-fluid">
	<a class="navbar-brand" href="{{ url_for('user_dashboard') }}">User Dashboard</a>
	<div class="d-flex flex-row-reverse">
		<div class="collapse navbar-collapse col-4 " id="navbarSupportedContent">
			<ul class="navbar-nav">
				<li class="nav-item p-2"><a class="nav-item btn btn-success" href="{{ url_for('all_shows') }}">All Shows</a></li>
				<li class="nav-item p-2"><a class="nav-item btn btn-success" href="{{ url_for('user_bookings') }}">Bookings</a></li>
				<li class="nav-item p-2"><a class="nav-item btn btn-success" href="#">Logout</a></li>
			</ul>
		</div>
	</div>
  </div>
</nav>
<div class="container">
	<div class="d-flex justify-content-center align-items-center">
		<div class="text-center my-5">
		  <h1>Hi Welcome!</h1>
		</div>
	</div>
	<div class="row justify-content-center m-2">
		<p class="fs-4 m-4 text-center">Search all the shows based on categories!</p>
		<form action="/user_dashboard/search" method="GET">
			<div class="row justify-content-center">
				<div class="col-2">
					<select class="form-control border border-success border-2" id="search_by" onchange="changeQuery();"  required>
						<option class="text-center" disabled selected value="">-- Search by --</option>
						{% for i in search_by_category %}
							<option class="text-center" value="{{i}}">Search by {{i}}</option>
						{% endfor %}
					</select>
				</div>

				<div class="col-8">
					<input class="form-control border border-success border-2" id="inputfield" name="search_query" list="dataOpt" autocomplete="off" placeholder="Type to search..." required>
					<datalist id="dataOpt"></datalist>
				</div>
			</div>
			<div class="row justify-content-center m-4">
				<div class="col-3 text-center">
					<button class="btn btn-success" type="submit">Search</button>
				</div>
			</div>
		</form>
	</div>
</div>
<HomeView>
	
</HomeView>
</body>
</template>

<!-- <style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->
