<template>
    <div :class="{navCollapsed:state.isSidebarNavCollapse}">
        <NAVLEFT class="sidebar theme-bg"></NAVLEFT>
        <NAVTOP ></NAVTOP>
    </div>
</template>
<script lang="ts">
import { defineComponent, reactive,computed } from 'vue';
import NAVTOP from "./component/navTop/navTop.vue";
import NAVLEFT from "./component/navLeft/navLeft.vue";
import {useStore} from "vuex";
export default defineComponent({
    setup() {
        let store=useStore();
        let state=reactive({
            isSidebarNavCollapse: computed(()=>store.getters.getIsSidebarNavCollapse),
        });
        return {
            state
        }
    },
    components:{
        NAVTOP,
        NAVLEFT
    }
})
</script>
