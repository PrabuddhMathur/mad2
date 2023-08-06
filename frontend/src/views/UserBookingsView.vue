<template>
    <UserBookings 
    :bookings=this.bookings
    />    
</template>
<script>
import axios from 'axios';
import UserBookings from '../components/UserBookings.vue';
    export default{
        name:'userBookingsView',
        components: {UserBookings},
        data(){
            return{
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                bookings:""
            }
        },
        methods: {
            async fetchBookings(){
                if (this.userSession){
                    axios.defaults.headers.common["Authorization"] = `Bearer ${this.userSession.token}`;
                    await axios
                    .get("http://127.0.0.1:8090/api/bookings")
                    .then((response)=>response)
                    .then((response)=>response.data)
                    .then((results)=>{
                        this.bookings=results;
                    })
                    this.$forceUpdate();
                } else {
                    console.log("Ducking user not logged in")
                }
            }
        },
        async beforeMount(){
            this.fetchBookings();
        }
    }
</script>