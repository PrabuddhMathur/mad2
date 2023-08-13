<template>
    <div class="modal fade" :id="venue.venue_id + 'edit_venue'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <form @submit.prevent="editVenue(venue.venue_id)">
        <div class="modal-dialog modal-md">
            <div class="modal-content" >
                <div class="modal-header" style="background-color: #BBE38F">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit Venue</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                    <div class="modal-body">
                        <div class="row justify-content-center text-center">
                            <div class="row m-1">
                                <h4>{{ venue.venue_name }}</h4>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4 align-self-center">Venue Name</label>
                                <input class="col-5" type="text" name="venue" v-model.trim="updated.venue_name">
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="">Place</label>
                                <input class="col-5" type="text" name="place" v-model.trim="updated.venue_place">
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="location">Location</label>
                                <select class='col-5' name="location" id="location" v-model="updated.venue_location">
                                    <option selected>{{ updated.venue_location }}</option>
                                    <option v-for="location in locations" :key="location">{{ location }}</option>
                                </select>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="">Capacity</label>
                                <input class="col-5" min="0" type="number" name="capacity" v-model=updated.venue_capacity>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-success">Save Edits</button>
                    </div>
            </div>
        </div>
    </form>
	</div>
</template>
<script>
import axios from 'axios'
    export default {
        props:{
            venues: {
                type: Object,
                required: true
            }
        },
        data(){
            return {
                locations : ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Jaipur', 'Kanpur', 'Kolkata', 'Lucknow', 'Mumbai', 'Nagpur', 'Patna', 'Pune', 'Surat', 'Thane', 'Vadodara', 'Varanasi', 'Bhopal', 'Coimbatore', 'Visakhapatnam'],
                venue:{
                    venue_id:this.venues.venue_id,
                    venue_name:this.venues.venue_name,
                },
                updated:{
                    venue_name:this.venues.venue_name,
                    venue_place:this.venues.venue_place,
                    venue_location:this.venues.venue_location,
                    venue_capacity:this.venues.venue_capacity,
                }
            
            }
        },
        methods:{
            async editVenue(venue_id){
                await axios
                    .put("http://127.0.0.1:8090/api/venue/"+venue_id,{
                        updated_venue_name:this.updated.venue_name,
                        updated_venue_place:this.updated.venue_place,
                        updated_venue_location:this.updated.venue_location,
                        updated_venue_capacity:this.updated.venue_capacity
                        })
                        location.href="/admin_dashboard"
            },
        }
    }
</script>