<template>
<form @submit.prevent="editShow">
    <div class="modal fade" :id="shows.show_id + 'view_show'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-md">
            <div class="modal-content" >
                <div class="modal-header" style="background-color: #BBE38F">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit Details</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row justify-content-center text-center">
                    <div class="row my-3">
                        <h4>{{ shows.show_name }}</h4>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4 align-self-center">Show Name</label>
                        <input class="col-6 disabled" type="text" name="show_name" @input="updated_name=$event.target.value" :value=shows.show_name>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="timing">Timing</label>
                        <select class="col-6" name="show_timing" id="timing" @input="updated_timing=$event.target.value">
                            <option :value=shows.show_timing selected>{{ shows.show_timing }}</option>
                            <option v-for="timing in timings" :key="timing" :value=timing>{{ timing }}</option>                                    
                        </select>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="genre">Genre</label>
                        <select class="col-6" name="show_tags" id="genre" @input="updated_genre=$event.target.value" >
                            <option :value=shows.show_tags>{{ shows.show_tags }}</option>
                            <option v-for="genre in genres" :key="genre" :value=genre>{{ genre }}</option>
                        </select>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="">Ticket Price</label>
                        <span class="col-1 input-group-addon">&#x20B9;</span>
                        <input class="col-5" min="0" type="number" name="show_price" :value=shows.show_ticketprice @input="updated_show_price=$event.target.value">
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="">Available Tickets</label>
                        <input class="col-6" min="0" :max=venues.venue_capacity type="number" name="available_tickets" :value=shows.available_tickets @input="updated_tickets=$event.target.value" required>
                    </div>
                </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-success">Save Edits</button>
                    <a  type="button" class="btn btn-danger" id="venue_btn"  @click="deleteShow">Delete</a>
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
            venues:{
                type: Object,
                required: true
            }
        },
        data(){
            return {
                show_id:this.shows.show_id,
                updated_name:"",
                updated_timing:"",
                updated_genre:"",
                updated_show_price:"",
                updated_tickets:"",
                genres:['Action', 'Comedy', 'Drama', 'Horror','Mythology', 'Romance', 'Science Fiction', 'Thriller', 'Fantasy', 'Animation', 'Adventure'],
                timings:['9AM - 12PM','12PM - 3PM','3PM - 6PM','6PM - 9PM','9PM - 12AM']
            }
        },
        methods:{
            async editShow(){
                await axios
                    .put("http://127.0.0.1:8090/api/show"+this.show_id,{
                        updated_name:this.updated_name,
                        updated_genre: this.updated_genre,
                        updated_timing:this.updated_timing,
                        updated_tickets:this.updated_tickets,
                        updated_show_price:this.updated_show_price,
                    })
            },
            async deleteShow(){
                await axios
                    .delete("http://127.0.0.1:8090/api/show/"+this.show_id)
                    this.$router.go(0);

            }
        }
    }
</script>