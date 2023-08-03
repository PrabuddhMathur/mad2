<template>
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
							<option class="text-center" v-for="i in search_by_category" :key="i" :value=i>Search by {{i}}</option>
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
</template>
<script>
	export default{
		data(){
			return {
				search_by_category: ['Show','Venue','Location','Timing', 'Genre','Rating' ]
			}
		}
	}
</script>