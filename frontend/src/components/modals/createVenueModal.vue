<template>
    <!-- Create Venue Modal -->
<div class="modal fade" id="create_venue" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-md">
      <div class="modal-content" >
        <div class="modal-header" style="background-color: #BBE38F">
          <h1 class="modal-title fs-5" id="staticBackdropLabel">Add Venue</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="addVenue">
          <div class="modal-body">
              <div class="row justify-content-center text-center">
                <div class="row m-1">
                    <h4>Creating a new venue.</h4>
                </div>
                <div class="row m-1">
                    <label class="form-label col-4 align-self-center">Venue Name</label>
                    <input class="col-5" type="text" name="venue" v-model.trim="venue_name" required>
                </div>
                <div class="row m-1">
                    <label class="form-label col-4" for="">Place</label>
                    <input class="col-5" type="text" name="place" v-model.trim="venue_place" required>
                </div>
                <div class="row m-1">
                    <label class="form-label col-4" for="location">Location</label>
                    <select class='col-5' name="location" id="location" v-model.trim="venue_location" required>
                      <option value="" selected>-- Select Location --</option>
                      <option v-for="location in locations" :key="location" :value=location>{{ location }}</option>
                    </select>
                </div>
                <div class="row m-1">
                    <label class="form-label col-4" for="">Capacity</label>
                    <input class="col-5" min="0" type="number" name="capacity" v-model.trim="venue_capacity" required>
                </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-success">Add</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
export default{
  name:"createVenueModal",
  data(){
    return {
      venue_name:"",
      venue_place:"",
      venue_location:"",
      venue_capacity:"",
      locations:['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Jaipur', 'Kanpur', 'Kolkata', 'Lucknow', 'Mumbai', 'Nagpur', 'Patna', 'Pune', 'Surat', 'Thane', 'Vadodara', 'Varanasi', 'Bhopal', 'Coimbatore', 'Visakhapatnam']
    }
  },
  methods:{
          async addVenue(){
              await axios
                .post("http://127.0.0.1:8090/api/venues",{
                  venue_name:this.venue_name,
                  venue_place:this.venue_place,
                  venue_location:this.venue_location,
                  venue_capacity:this.venue_capacity
                })
                location.href="/admin_dashboard"
          }
      }
}
</script>
