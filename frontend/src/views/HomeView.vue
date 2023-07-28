<template>
    <div>
      <p>
        {{this.data}}
      </p>

    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    
    
    name: "HomeView",
    data() {
      return {
        data: null,
      };
    },
    methods: {
      updateComments() {
        this.fetchData();
      },
      async fetchData() {
        await axios
          .get("http://127.0.0.1:8090/admin_dashboard")
          .then((response) => response)
          .then((result) => {
            data=result.data
            console.log(result)
          })
          .catch(() => {
            // console.error("Error fetching data:", error);
          });
      },
    },
    async beforeMount() {
      this.fetchData();
    },
  };
  </script>
  