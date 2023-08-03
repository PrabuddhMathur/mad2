
<template>
	<div>
		<div v-if="this.ifVenues">
			<AdminDashboardComp
			:venues="this.venues"
			/>
		</div>
	</div>
	
</template>
<script>
import AdminDashboardComp from "@/components/AdminDashboard.vue";
import axios from "axios";
import { resolveDynamicComponent } from 'vue';
export default {
	name: 'adminDashboardView',
	components: {AdminDashboardComp},
    data() {
        return {
			userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            venues: null,
        }
    },
    methods: {
            async fetchVenues(){
            await axios 
                .get('http://127.0.0.1:8090/api/venues')
				.then((response) => response)
				.then((response) => response.data)
                .then((results)=>{
					this.venues = results;

                })
                .catch(()=>{
                    console.error("MFing Venue error: ", error)
                });
				this.$forceUpdate();
			},
			async isAdmin(){
				if (this.userSession){

					axios.defaults.headers.common[
				"Authorization"
				] = `Bearer ${this.userSession.token}`;

				await axios
					.get('http://127.0.0.1:8090/api/isadmin')
					.then((response)=>response)
					.then((response)=>response.data)
					.then((response)=>{
						
						var bool = response[0]
						if (! bool){
							location.href="/"
						}
					})
				}
				else{
					location.href="/"
				}
			}
    },
    computed: {
		getVenues(){
			return this.venues;
		},
		ifVenues() {
			if (this.getVenues != null) {
				return true
			} else {
				return false
			}
		}
	},
	async beforeMount() {
		this.fetchVenues();
		this.isAdmin();
	},
	mounted() {
		document.title = "Admin Dashboard";
	},
}
</script>