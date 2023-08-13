<template>
    <div class="modal fade" :id="shows.show_id +'create_booking'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
        
        <div class="modal-content" >
            <div class="modal-header" style="background-color: #BBE38F">
                <h1 class="modal-title fs-5" id="staticBackdropLabel">Book Show</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="createBooking">
                <div class="modal-body">
                    <div class="container">
                        <div class="row text-center">
                            <h4 class="col-12 modal-title">{{ shows.show_name }}</h4>
                        </div>
                        <div class="row justify-content-center">
                            <p class="col-4 modal-title">Tickets</p>
                            <input class="col-4" min="1" :max=shows.available_tickets type="number" name="booking_tickets" v-model="tickets">
                        </div>
                        <div class="row justify-content-center">
                            <p class="col-4 modal-title">Price</p>
                            <p class="col-4 modal-title">₹{{ shows.show_ticketprice }}</p>
                        </div>
                        <div class="row justify-content-center">
                            <p class="col-4 modal-title">Total</p>
                            <p class="col-4 modal-title">₹{{ shows.show_ticketprice*this.tickets }}</p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-success">Book</button>
                </div>
            </form>
        </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
    export default {
        props: {
            shows:{
                type: Object,
                required: true
            }
        },
        data(){
            return {
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                tickets : ""
            }
        },
        methods:{
            async createBooking(){
                if (this.userSession){
					axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;

                    await axios 
                    .post("http://127.0.0.1:8090/api/bookings",{
                        tickets:this.tickets,
                        show_id:this.shows.show_id
                    })
                    location.href="/bookings"
            }
        }
    }
}
</script>