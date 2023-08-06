<template>
    <div class="container">
        <div class="d-flex justify-content-center align-items-center">
            <div class="text-center my-5">
            <h1>Hi Welcome!</h1>
            </div>
        </div>
		<form @submit.prevent="searchQuery(this.query)">
        <div class="row justify-content-center m-2">
            <p class="fs-4 m-4 text-center">Search all the shows based on categories!</p>
                <div class="row justify-content-center">
                    <div class="col-2">
                        <select class="form-control border border-success border-2" id="search_by" v-model="category" @change.prevent="this.refreshQuery()" required>
                            <option class="text-center" disabled selected value="">-- Search by --</option>
                            <option class="text-center" v-for="category in search_by_category" :key=category :value=category>Search by {{category}}</option>
                        </select>
                    </div>
                    <div class="col-8">
                        <input class="form-control border border-success border-2" name="query" list="dataOpt" autocomplete="off" placeholder="Type to search..." v-model.trim.lazy="query" required >
                            <datalist v-if="this.category === 'Show'" id="dataOpt">
                                <option v-for="show in this.shows" :key="show" :value=show.show_name>{{ show.show_name }}</option>
                            </datalist>
                            <datalist v-else-if="this.category ==='Venue'" id="dataOpt">
                                <option v-for="venue in this.venues" :key="venue" :value=venue.venue_name>{{ venue.venue_name }}</option>
                            </datalist>
                            <datalist v-else-if="this.category ==='Location'" id="dataOpt">
                                <option v-for="venue in this.venues" :key="venue" :value=venue.venue_location>{{ venue.venue_location }}</option>
                            </datalist>
                            <datalist v-else-if="this.category ==='Timing'" id="dataOpt">
                                <option v-for="show in this.shows" :key="show" :value=show.show_timing>{{ show.show_timing }}</option>
                            </datalist>
                            <datalist v-else-if="this.category==='Genre'" id="dataOpt">
                                <option v-for="show in this.shows" :key="show" :value=show.show_tags>{{ show.show_tags }}</option>
                            </datalist>
                            <datalist v-else-if="this.category==='Rating'" id="dataOpt">
                                <option v-for="show in this.shows" :key="show" :value=show.show_rating>{{ show.show_rating }}</option>
                            </datalist>
                    </div>
                </div>
                <div class="row justify-content-center m-4">
                    <div class="col-3 text-center">
                        <button class="btn btn-success">Search</button>
                    </div>
                </div>
        </div>
		</form>
		<searchByGenre
		v-if="this.category==='Genre'  && this.query!=''" 
		:results=this.results
		/>
		<searchByLocation
		v-if="this.category==='Location' && this.query!=''"
		:results=this.results
		/>
		<searchByVenue
		v-if="this.category==='Venue' && this.query!='' "
		:results=this.results
		/>
		<searchByTiming
		v-if="this.category==='Timing' && this.query!='' "
		:results=this.results
		/>
		<searchByShow
		v-if="this.category==='Show' && this.query!=''"
		:results=this.results
		/>
		<searchByRating
		v-if="this.category==='Rating' && this.query!='' "
		:results=this.results
		/>
	</div>
</template>

<script>
import axios from 'axios';
import searchByGenre from '../components/search/searchByGenre.vue';
import searchByLocation from '../components/search/searchByLocation.vue';
import searchByRating from '../components/search/searchByRating.vue';
import searchByShow from '../components/search/searchByShow.vue';
import searchByTiming from '../components/search/searchByTiming.vue';
import searchByVenue from '../components/search/searchByVenue.vue';

export default{
    components:{searchByGenre,searchByLocation,searchByRating,searchByShow,searchByTiming,searchByVenue},

    data(){
			return {
				search_by_category: ['Show','Venue','Location','Timing', 'Genre','Rating' ],
                shows:"",
                category:"",
                venues:"",
                query:"",
                results:"",
			}
		},
    methods:{
        async fetchShows(){
        await axios 
            .get('http://127.0.0.1:8090/api/shows')
            .then((response) => response)
            .then((response) => response.data)
            .then((results)=>{
                this.shows = results;

            })
            .catch(()=>{
                console.error("MFing Show error: ", error)
            });
            this.$forceUpdate();
        },
        async fetchVenues(){
        await axios 
            .get('http://127.0.0.1:8090/api/venues')
            .then((response) => response)
            .then((response) => response.data)
            .then((results)=>{ 
                this.venues = results;

            })
            .catch(()=>{
                console.error("MFing Venue error: ", error)
            });
            this.$forceUpdate();
        },
        async searchQuery(query){
            await axios
                .post('http://127.0.0.1:8090/api/search',{
                    category:this.category,
                    query:query
                })
                .then((response)=>response)
                .then((response)=>response.data)
                .then((results)=>{
                    // console.log(results)
                    this.results=results;
                })
				this.state=true
                this.$forceUpdate();

        },
		async refreshQuery(){
			this.query=""
			document.getElementsByName('query').innerHTML="";
		}
    },
	computed:{
		ifResults() {
			if (this.results != null) {
				return true
			} else {
				return false
			}
		}
	},
    async beforeMount(){
        this.fetchShows();
        this.fetchVenues();
    },
    mounted(){
        document.title="Search"
    }
}
</script>