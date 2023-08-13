<template>
    <div class="modal fade" :id="booking.booking_id + 'show_rating'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-md">
            <div class="modal-content">
                <div class="modal-header" style="background-color: #D6ECA4">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel" >Rate {{ booking.show_details.show_name }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="createRating">
                    <div class="modal-body">
                        <div class="row justify-content-center">
                            <div v-for="index in 10" :key="index" class="col-1">
                                <input type="radio" class="form-check-input" :id="'rating'+index" name="rating" :value="index" v-model=rating>
                                <label :for="'rating'+index">{{index}}</label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Close</button>
                        <button class="btn btn-success" type="submit">Submit Rating</button>
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
                type:Object,
                required: true
            }
        },
        data() {
            return {
                rating:""
            }
        },
        methods:{
            async createRating(){
                await axios
                    .post("http://127.0.0.1:8090/api/rating" , {
                        rating:this.rating,
                        booking_id:this.booking.booking_id
                    })
                    location.href="/bookings"
            }
        }
    }
</script>