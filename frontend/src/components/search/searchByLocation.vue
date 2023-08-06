<template>
    <div class="col-4 m-1 p-1">
        <template v-for="venue in this.getResults" :key="venue">
            <template v-for="show in venue.venue_show" :key="show">
                <div class="card">
                    <div class="card-header" style="background-color: #D6ECA4">
                        <h5 class="card-title">{{ venue.venue_name }}</h5>
                    </div>
                    <div class="card-body">
                        <div class="row justify-content-center">
                            <div class="col-5 text-end ">
                                <p class="card-text m-1 text-nowrap">Show :</p>
                                <p class="card-text m-1 text-nowrap">Location :</p>
                                <p class="card-text m-1 text-nowrap">Timing :</p>
                                <p class="card-text m-1 text-nowrap">Genre :</p>
                                <p class="card-text m-1 text-nowrap">Rating :</p>
                                <p class="card-text m-1 text-nowrap">Ticket Price :</p>
                                <p class="card-text m-1 text-no-wrap">Available Tickets :</p>
                            </div>
                            <div class="col-5 text-start">
                                <p class="card-text m-1 text-nowrap">{{ show.show_name }}</p>
                                <p class="card-text m-1 text-nowrap" >{{ venue.venue_location }}</p>
                                <p class="card-text m-1 text-nowrap">{{ show.show_timing }}</p>
                                <p class="card-text m-1 text-nowrap">{{ show.show_tags }}</p>
                                <p class="card-text m-1 text-nowrap">{{ show.show_rating }}</p>
                                <p class="card-text m-1 text-nowrap">&#x20B9;{{ show.show_ticketprice }}</p>
                                <p class="card-text m-1 text-nowrap">{{ show.available_tickets }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div class="row justify-content-center">
                            <button class="btn btn-success" data-bs-toggle="modal" :data-bs-target="'#'+ show.show_id +'create_booking'">Book</button>
                        </div>
                        <!--Create Booking Modal-->
                        <createBookingModal :shows=show />
                    </div>
                </div>
            </template>
        </template>
    </div>
</template>
<script>
import createBookingModal from '../modals/createBookingModal.vue';
export default {
    components:{createBookingModal},
    props:{
        results:{
            type : Array,
            required:true
        }
    },
    computed:{
        getResults(){
                return this.results
            }
    }
}
</script>