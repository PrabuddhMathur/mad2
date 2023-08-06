<template>
    <div class="container-fluid">
        <div class="row justify-content-center">
            <template v-for="booking in this.bookings" :key="booking">
                <div class="card col-3 m-2 p-0" >
                    <div class="card-header" style="background-color: #D6ECA4">
                        <h5 class="card-text">{{ booking.show_details.show_name }}</h5>
                    </div>

                    <div class="card-body">
                        <div class="row">
                            <div class="col-6">
                                <p class="card-text text-end m-1 text-nowrap">Venue : </p>
                                <p class="card-text text-end m-1 text-nowrap">Location : </p>
                                <p class="card-text text-end m-1 text-nowrap">Tickets Booked : </p>
                                <p class="card-text text-end m-1 text-nowrap">Show Timing : </p>
                                <p class="card-text text-end m-1 text-nowrap">Your rating : </p>
                            </div>

                            <div class="col-6">
                                <p class="card-text text-start m-1 text-nowrap">{{ booking.venue_details.venue_name }}</p>
                                <p class="card-text text-start m-1 text-nowrap">{{ booking.venue_details.venue_location }}</p>
                                <p class="card-text text-start m-1 text-nowrap">{{ booking.booking_tickets }}</p>
                                <p class="card-text text-start m-1 text-nowrap">{{ booking.show_details.show_timing }}</p>
                                <p class="card-text text-start m-1 text-nowrap">{{ booking.user_rating }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer">
                    <div class="container">
                        <div class="row">
                            <button class="btn btn-success m-2" data-bs-toggle="modal" :data-bs-target="'#'+booking.booking_id+'edit_booking'">Edit Booking details</button>
                            <button class="btn btn-success m-2" data-bs-toggle="modal" :data-bs-target="'#'+booking.booking_id+'show_rating'">Rate Show</button>
                            <!-- Edit Bookings Modal -->
                            <editBookingsModel :booking=booking />
                            <!--Rate Show Modal-->
                            <rateShowModal :booking=booking />
                        </div>
                    </div>
                </div>
                </div>
            </template>
        </div>
    </div>
</template>
<script>
import rateShowModal from './modals/rateShowModal.vue';
import editBookingsModel from './modals/editBookingsModel.vue';
    export default{
        components: {rateShowModal,editBookingsModel},
        props:{
            bookings:{
                type: Array,
                required: true
            }
        }
    }
</script>