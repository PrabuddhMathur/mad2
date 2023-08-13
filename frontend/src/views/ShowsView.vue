<template>
    	<div class="container-fluid">
		<div class="row">
			<div class="h3 m-2 col text-center">All Shows</div>
		</div>
		<div v-for="venue in this.getVenues" :key="venue">
            <div class="card m-1">
                <div class="card-header" style="background-color: #BBE38F">
                    <h5 class="card-title">Venue : {{ venue.venue_name }} {{ venue.venue_location }}</h5>
                </div>
                <div class="card-body">
                    <div class="container ">
                        <div v-if="venue.venue_show.length>0" class="row align-items-center">
                            <div v-for="show in venue.venue_show" :key="show" class="card m-2 col-3 p-0">
                                <div class="card-header" style="background-color: #BBE38F">
                                    <h5 class="card-title m-1">{{ show.show_name }}</h5>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-7 text-start">
                                            <p class="card-text m-1">Timing :</p>
                                            <p class="card-text m-1">Genre :</p>
                                            <p class="card-text m-1">Rating :</p>
                                            <p class="card-text m-1">Ticket Price :</p>
                                            <p class="card-text m-1">Available Tickets :</p>
                                        </div>
                                        <div class="col-5 text-start">
                                            <p class="card-text m-1">{{ show.show_timing }}</p>
                                            <p class="card-text m-1">{{ show.show_tags }}</p>
                                            <p class="card-text m-1">{{ show.show_rating }}</p>
                                            <p class="card-text m-1">&#x20B9;{{ show.show_ticketprice }}</p>
                                            <p class="card-text m-1">{{ show.available_tickets }}</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="card-footer">
                                    <div class="row justify-content-center">
                                        <button v-if="show.available_tickets==0" class="btn btn-secondary" disabled>HOUSEFULL</button>
                                        <button v-else class="btn btn-success" data-bs-toggle="modal" :data-bs-target="'#' + show.show_id + 'create_booking'">Book</button>
                                        <createBookingModal 
                                        :shows=show
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else>No available shows</div>
                    </div>
                </div>
            </div>
        </div>
		
	</div>

</template>
<script>
import createBookingModal from '../components/modals/createBookingModal.vue';
import axios from 'axios';
export default {
    components: {createBookingModal},
    name: "allShowsComp",
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
		}
	},
	async beforeMount() {
		this.fetchVenues();
	},
	mounted() {
		document.title = "All Shows";
	},
}
</script>