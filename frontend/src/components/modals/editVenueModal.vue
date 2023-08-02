<template>
    <div class="modal fade" :id="venues.venue_id + 'edit_venue'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-md">
            <div class="modal-content" >
                <div class="modal-header" style="background-color: #BBE38F">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit Venue</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                    <div class="modal-body">
                        <div class="row justify-content-center text-center">
                            <div class="row m-1">
                                <h4>{{ venues.venue_name }}</h4>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4 align-self-center">Venue Name</label>
                                <input class="col-5" type="text" name="venue" :value=venues.venue_name>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="">Place</label>
                                <input class="col-5" type="text" name="place" :value=venues.venue_place>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="location">Location</label>
                                <select class='col-5' name="location" id="location">
                                    <option selected>{{ venues.venue_location }}</option>
                                    <!-- {% for location in locations %}
                                    <option value="{{ location }}">{{ location }}</option>
                                    {% endfor %} -->
                                </select>
                            </div>
                            <div class="row m-1">
                                <label class="form-label col-4" for="">Capacity</label>
                                <input class="col-5" min="0" type="number" name="capacity" :value=venues.venue_capacity>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-success" @onclick="editVenue(venues.venue_id)">Save Edits</button>
                    </div>
            </div>
        </div>
	</div>
</template>
<script>
    export default {
        props:{
            venues: {
                type: Object,
                required: true
            }
        },
        data(){
            return {
            venue_name:"",
            venue_place:"",
            venue_location:"",
            venue_capacity:""
            }
        },
        methods:{
            async editVenue(venue_id){
                await axios
                    .put("http://127.0.0.1:8090/api/venue/"+venue_id,{
                        venue_name:this.venue_name,
                        venue_place:this.venue_place,
                        venue_location:this.venue_location,
                        venue_capacity:this.venue_capacity
                        })
                        location.href="/admin_dashboard"
            },
        }
    }
</script>