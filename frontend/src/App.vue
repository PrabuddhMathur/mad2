<script setup>
import { RouterLink, RouterView } from 'vue-router'
import navBar from './components/navBar.vue'
</script>

<template>
<body>
	<navBar></navBar>
	<router-view></router-view>
</body>
</template>