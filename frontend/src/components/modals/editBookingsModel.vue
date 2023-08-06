<template>
<div class="modal fade" :id="booking.booking_id + 'edit_booking'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-md">
        <div class="modal-content">
            <div class="modal-header" style="background-color: #D6ECA4">
                <h1 class="modal-title fs-5" id="staticBackdropLabel">Edit booking for {{ booking.show_details.show_name }}</h1>
                <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="POST">
                <div class="modal-body">
                    <div class="container">
                        <div class="row text-center">
                            <h4 class="col-12 modal-title">{{ booking.show_details.show_name }}</h4>
                        </div>
                        <div class="row justify-content-center m-2">
                            <p class="col-4 modal-title">Tickets booked</p>
                            <input class="col-4" min="1" type="number" name="booking_tickets"  :value=booking.show_details.booking_tickets required>
                        </div>
                        <div class="row justify-content-center m-2">
                            <p class="col-4 modal-title">Price</p>
                            <input class="col-4" type="number" min="0" :value=booking.show_details.show_ticketprice disabled>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Close</button>
                    <button class="btn btn-success" type="submit">Save Edits</button>
                    <a type="button" class="btn btn-danger" id="venue_btn">Delete</a>
                </div>
        </form>
        </div>
    </div>
</div>
</template>
<script>
    export default{
        props:{
            booking:{
                type: Object,
                required: true
            }
        }
    }
</script>