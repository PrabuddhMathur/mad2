<template>
    <div class="modal fade" :id="shows.show_id + 'view_show'" data-bs-backdrop="static" data-bs-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-md">
            <div class="modal-content" >
                <div class="modal-header" style="background-color: #BBE38F">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit Details</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form :action="'/edit/show/'+shows.show_id" method="POST">
                <div class="modal-body">
                    <div class="row justify-content-center text-center">
                    <div class="row my-3">
                        <h4>{{ shows.show_name }}</h4>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4 align-self-center">Show Name</label>
                        <input class="col-6 disabled" type="text" name="show_name" :value=shows.show_name>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="timing">Timing</label>
                        <select class="col-6" name="show_timing" id="timing">
                            <option selected>{{ shows.show_timing }}</option>
                            <!-- {% for timing in timings %}
                            <option value="{{ timing }}">{{ timing }}</option>
                            {% endfor %} -->
                        </select>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="genre">Genre</label>
                        <select class="col-6" name="show_tags" id="genre">
                            <option>{{ shows.show_tags }}</option>
                            <!-- {% for genre in genres %}
                            <option value="{{ genre }}">{{ genre }}</option>
                            {% endfor %} -->
                        </select>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="">Ticket Price</label>
                        <span class="col-1 input-group-addon">&#x20B9;</span>
                        <input class="col-5" min="0" type="number" name="show_price" :value=shows.show_ticketprice>
                    </div>
                    <div class="row m-1">
                        <label class="form-label col-4" for="">Available Tickets</label>
                        <input class="col-6" min="0" :max=venues.venue_capacity type="number" name="available_tickets" :value=shows.available_tickets required>
                    </div>
                </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-success">Save Edits</button>
                    <a  :href="'/delete/show/'+ shows.show_id " type="button" class="btn btn-danger" id="venue_btn">Delete</a>
                </div>
            </form>
            </div>
        </div>
    </div>
</template>
<script>
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
    }
</script>