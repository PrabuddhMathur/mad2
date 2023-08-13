<template>
    <div class="container">
		<div class="row justify-content-center">
			<div class="col-6">
				<img src="http://127.0.0.1:8090/static/show_details.png" alt="">
				<strong><p class="text-center">Show Summary</p></strong>
			</div>
			<div class="col-6">
				<img src="http://127.0.0.1:8090/static/venue_details.png"  alt="">
				<strong><p class="text-center">Venue Summary</p></strong>
			</div>
		</div>
	  </div>
</template>
<script>
import axios from 'axios'
export default{
    data() {
        return {
			userSession: JSON.parse(localStorage.getItem("userSession")) || null,
        }
    },

    methods:{
        async fetchPhotos(){
            await axios
                .get("http://127.0.0.1:8090/api/admin_summary")
                .then((response)=>response)
        },
        async isAdmin(){
				if (this.userSession){
					axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;

				await axios
					.get('http://127.0.0.1:8090/api/isadmin')
					.then((response)=>response)
					.then((response)=>response.data)
					.then((response)=>{
						
						var bool = response[0]
						if (! bool){
							location.href="/shows"
						}
					})
				}
				else{
					location.href="/login"
				}
			}
    },
    async beforeMount(){
        this.isAdmin();
        this.fetchPhotos();
    },
    mounted(){
        document.title="Admin Summary"
    },
    
}
</script>