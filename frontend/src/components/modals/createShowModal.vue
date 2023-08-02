<template>
    <div class="modal fade" :id="venues.venue_id + 'create_show'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        
        <div class="modal-dialog modal-md">
            <div class="modal-content" >
                <div class="modal-header" style="background-color: #BBE38F">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Add Show</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                
                    <div class="modal-body">
                        <div class="row justify-content-center text-center">
                            <div class="row my-3">
                                <h4>Creating a new show.</h4>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4 align-self-center">Show Name</label>
                                <input class="col-6" type="text" name="show_name" v-model="show_name" required>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="timing">Timing</label>
                                <select class="col-6" name="show_timing" id="timing" v-model="show_timing" required>
                                    <option value="" disabled selected>-- Select Timing --</option>
                                    <option value="9-12">9-12</option>
                                    <option value="12-3">12-3</option>
                                    
                                    <!-- <option value="{{ timing }}">{{ timing }}</option> -->
                                    
                                </select>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="genre">Genre</label>
                                <select class="col-6" name="show_tags" id="genre" v-model="show_tags" required>
                                    <option value="" disabled selected>-- Select Genre --</option>
                                    <option value="Action">Action</option>
                                    <option value="Comedy">Comedy</option>
                                    <option value="Mythology">Mythology</option>
                                    
                                    <!-- <option value="{{ genre }}">{{ genre }}</option> -->
                                   
                                </select>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="">Ticket Price</label>
                                <span class="col-1 input-group-addon">&#x20B9;</span>
                                <input class="col-5" min="0" type="number" name="show_price" v-model="show_ticketprice" required>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="">Available Tickets</label>
                                <input class="col-6" min="0" :max=venues.venue_capacity type="number" name="available_tickets" v-model="available_tickets" required>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-success" @click="addShow">Add</button>
                    </div>
               
            </div>
        </div>
	</div>
</template>
<script>
import axios from 'axios';
    export default {
        props:{
            venues: {
                type: Object,
                required: true
            }
        },
        data(){
        return {
            venue_id:this.venues.venue_id,
            show_name:"",
            show_timing:"",
            show_tags:"",
            show_ticketprice:"",
            available_tickets:""
        }
        },
        methods:{
            async addShow(){
                await axios
                    .post("http://127.0.0.1:8090/api/shows",{
                        venue_id:this.venue_id,
                        show_name:this.show_name,
                        show_timing:this.show_timing,
                        show_tags:this.show_tags,
                        show_ticketprice:this.show_ticketprice,
                        available_tickets:this.available_tickets
                    })
                    location.href="/admin_dashboard"
            }
        }
    }
</script>