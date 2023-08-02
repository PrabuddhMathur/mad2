
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
export default {
	name: 'adminDashboardView',
	components: {AdminDashboardComp},
    data() {
        return {
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
	},
	mounted() {
		document.title = "Admin Dashboard";
	},
}
</script>