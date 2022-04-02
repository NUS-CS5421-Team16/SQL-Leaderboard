<template>
  <router-view />
</template>
<script lang="ts">
import { defineComponent, nextTick, onMounted, createApp } from 'vue'
export default defineComponent({
  setup(props) {
    let theme = window.localStorage.getItem("theme");
    theme && window.document.documentElement.setAttribute("data-ming", theme);
  },
})
</script>

<style lang="scss">
* {
  margin: 0;
}
</style>
