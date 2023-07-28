<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script>
import axios from "axios";
export default {
  
  
  name: "AboutView",
  data() {
    return {
      test: null,
    };
  },
  methods: {
    updateComments() {
      this.fetchData();
    },
    async fetchData() {
      await axios
        .get("http://127.0.0.1:8090/")
        .then((response) => response)
        .then((result) => {
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
