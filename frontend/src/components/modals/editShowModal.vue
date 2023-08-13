<template>
<form @submit.prevent="this.editShow()">
    <div class="modal fade" :id="show.show_id + 'view_show'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-md">
            <div class="modal-content" >
                <div class="modal-header" style="background-color: #BBE38F">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit Details</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row justify-content-center text-center">
                    <div class="row my-3">
                        <h4>{{ show.show_name }}</h4>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4 align-self-center">Show Name</label>
                        <input class="col-6 disabled" type="text" name="show_name" v-model="updated.show_name"  required>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="timing">Timing</label>
                        <select class="col-6" name="show_timing" id="timing" v-model="updated.show_timing" required>
                            <option :value=updated.show_timing>{{ updated.show_timing }}</option>
                            <option v-for="timing in timings" :key="timing" :value=timing>{{ timing }}</option>                                    
                        </select>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="genre">Genre</label>
                        <select class="col-6" name="show_tags" id="genre" v-model="updated.show_tags" required>
                            <option :value=updated.show_tags>{{ updated.show_tags }}</option>
                            <option v-for="genre in genres" :key="genre" :value=genre>{{ genre }}</option>
                        </select>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="">Ticket Price</label>
                        <span class="col-1 input-group-addon">&#x20B9;</span>
                        <input class="col-5" min="0" type="number" name="show_price" v-model="updated.show_ticketprice" required>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="">Available Tickets</label>
                        <input class="col-6" min="0" :max=this.capacity type="number" v-model="updated.available_tickets" required>
                    </div>
                </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-success">Save Edits</button>
                    <a type="button" class="btn btn-danger" id="venue_btn"  @click="deleteShow">Delete</a>
                </div>
            </div>
        </div>
    </div>
</form>
</template>
<script>
import axios from 'axios';
    export default {
        props:{
            shows: {
                type: Object,
                required: true
            },
            capacity:{
                type: Number,
                required: true
            }
        },
        data(){
            return {
                show:{
                    show_id:this.shows.show_id,
                    show_name:this.shows.show_name,
                },

                updated:{
                    show_name:this.shows.show_name,
                    show_timing:this.shows.show_timing,
                    show_tags:this.shows.show_tags,
                    show_ticketprice:this.shows.show_ticketprice,
                    available_tickets:this.shows.available_tickets

                },

                genres:['Action', 'Comedy', 'Drama', 'Horror','Mythology', 'Romance', 'Science Fiction', 'Thriller', 'Fantasy', 'Animation', 'Adventure'],
                timings:['9AM - 12PM','12PM - 3PM','3PM - 6PM','6PM - 9PM','9PM - 12AM']
            }
        },
        methods:{
            async editShow(){
                await axios
                    .put("http://127.0.0.1:8090/api/show/"+this.show.show_id,{
                        updated_name:this.updated.show_name,
                        updated_genre: this.updated.show_tags,
                        updated_timing:this.updated.show_timing,
                        updated_tickets:this.updated.available_tickets,
                        updated_show_price:this.updated.show_ticketprice,
                    })
                    location.href="/admin_dashboard"
            },
            async deleteShow(){
                await axios
                    .delete("http://127.0.0.1:8090/api/show/"+this.show.show_id)
                    this.$router.go(0);

            },
        },
    }
</script>