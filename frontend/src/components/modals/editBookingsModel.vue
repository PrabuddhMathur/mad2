<template>
<div class="modal fade" :id="booking.booking_id + 'edit_booking'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-md">
        <div class="modal-content">
            <div class="modal-header" style="background-color: #D6ECA4">
                <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit booking for {{ booking.show_details.show_name }}</h1>
                <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="updateBooking">
                <div class="modal-body">
                    <div class="container">
                        <div class="row text-center">
                            <h4 class="col-12 modal-title">{{ booking.show_details.show_name }}</h4>
                        </div>
                        <div class="row justify-content-center m-2">
                            <p class="col-4 modal-title">Tickets booked</p>
                            <input class="col-4" min="1" :max="booking.show_details.available_tickets+this.updated_tickets" type="number" name="booking_tickets"  v-model="this.updated_tickets" required>
                        </div>
                        <div class="row justify-content-center m-2">
                            <p class="col-4 modal-title">Price</p>
                            <input class="col-4" type="number" min="0" :value=booking.show_details.show_ticketprice disabled>
                        </div>
                        <div class="row justify-content-center m-2">
                            <p class="col-4 modal-title">Price</p>
                            <input class="col-4" type="number" :value=booking.show_details.show_ticketprice*this.updated_tickets disabled>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Close</button>
                    <button class="btn btn-success" type="submit">Save Edits</button>
                    <a type="button" class="btn btn-danger" @click="deleteBooking" id="venue_btn">Delete</a>
                </div>
        </form>
        </div>
    </div>
</div>
</template>
<script>
import axios from 'axios'
    export default{
        props:{
            booking:{
                type: Object,
                required: true
            }
        },
        data(){
            return {
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                updated_tickets : this.booking.booking_tickets
            }
        },
        methods:{
            async updateBooking(){
                if (this.userSession){
					axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;

                    await axios 
                    .put("http://127.0.0.1:8090/api/bookings",{
                        tickets:this.updated_tickets,
                        booking_id:this.booking.booking_id
                    })
                    location.href="/bookings"
                }   
            },
            async deleteBooking(){
                if (this.userSession){
					axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;

                    await axios 
                    .delete("http://127.0.0.1:8090/api/bookings/" +this.booking.booking_id,)
                    location.href="/bookings"
                }
            }
        }
    }
</script>