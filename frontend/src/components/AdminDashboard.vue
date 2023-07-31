
<template>
    <div class="container-fluid">
	<div class="card m-2">
		<div class="card-header" style="background-color: #BBE38F">
			<h4 class="card-title text-center">Venues</h4>
		</div>
		<div class="card-body">
			<div class="container-fluid">
				<div class="row justify-content-center">
					<button class="col-4 btn btn-success col-sm-auto mb-2" data-bs-toggle="modal" data-bs-target="#create_venue">Create Venue</button>
				</div>
                <createVenueModal />
				<div class="row justify-content-center">
					
					<div v-for="venue in this.getVenues" :key="venue" class="row">
						<div class="card m-2 p-0">
							<div class="card-header" style="background-color: #BBE38F">
								<div class="row">
									<h5 class="col-10 card-title align-self-center">{{ venue.venue_name }}</h5>
									<button class="col-2 btn btn-success" data-bs-toggle="modal"  :data-bs-target="'#'+venue.venue_id + 'create_show'">Add Show</button>
									<createShowModal
									:venues=venue
									/>
								</div>
							</div>
							<div class="card-body">
								<div class="container">
									<div class="row justify-content-center">
										<p class="col-12 card-text text-center h6">Available capacity: {{ venue.venue_capacity }}</p>
										<p class="col-12 card-text text-center h6">Available Shows</p>
									</div>
									<div class="row">
									
									<div  v-for="show in venue.venue_show" :key="show" class="card col-3 m-4 p-0">
										<div class="card-header p-2" style="background-color: #BBE38F">
											<div class="row justify-content-center">
												<h6 class="col-6 card-title text-center m-0">{{ show["show_name"] }}</h6>
											</div>
										</div>
										<div class="card-body">
											<div class="row">
												<div class="col-7 text-start">
													<p class="card-text m-1">Timing :</p>
													<p class="card-text m-1">Genre :</p>
													<p class="card-text m-1">Rating :</p>
													<p class="card-text m-1">Ticket Price :</p>
													<p class="card-text m-1">Available Tickets :</p>
												</div>
												<div class="col-5 text-start">
													<p class="card-text m-1">{{ show.show_timing }}</p>
													<p class="card-text m-1">{{ show.show_tags }}</p>
													<p class="card-text m-1">{{ show.show_rating }}</p>
													<p class="card-text m-1">&#x20B9;{{ show.show_ticketprice }}</p>
													<p class="card-text m-1">{{ show.available_tickets }}</p>
												</div>
											</div>
										</div>
										<div class="card-footer">
											<div class="row">
												<button class="col-12 btn btn-success" data-bs-toggle="modal" :data-bs-target="'#' + show.show_id +'view_show'">Edit Details</button>
												<editShowModal 
												:shows=show
												:venues=venue
												/>
											</div>
										</div>
									</div>
									
									</div>
								</div>
							</div>
							<div class="card-footer">
								<div class="row justify-content-center">
									<button class="col-3 btn btn-success m-2" data-bs-toggle="modal" :data-bs-target="'#'+venue.venue_id+'edit_venue'">Edit Venue</button>
									<a  href="/delete/venue/{{ venue.venue_id }}" type="button" class="col-3 btn btn-danger m-2" id="venue_btn">Delete Venue</a>
									<editVenueModal :venues=venue />
								</div>

							</div>
						</div>
					</div>
					
				</div>
			</div>
		</div>
		
	</div>

</div>
</template>
<script>
import createVenueModal from "@/components/modals/createVenueModal.vue";
import createShowModal from "@/components/modals/createShowModal.vue";
import editVenueModal from "@/components/modals/editVenueModal.vue";
import editShowModal from "@/components/modals/editShowModal.vue"

    export default {
		components: {createShowModal,createVenueModal, editVenueModal ,editShowModal},
        name: "adminDashboardComp",
        props:{
            venues: {
                type: Array,
                required: true
            }
        },
		// data() {
		// 	return {
		// 	shouldRenderComponent: false,
		// 	};
		// },
        computed:{
            getVenues(){
                return this.venues
            }
        },
		// mounted(){
		// 	this.shouldRenderComponent = true;
		// }
    }
</script>