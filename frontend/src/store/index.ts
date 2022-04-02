import { createStore } from "vuex";
import mutations from "./mutations";
import actions from "./actions";
import getters from "./getters";
export default createStore({
    state: {
        permissionList: null ,
        sidebarMenu: [] ,
        currentMenu: "" ,
        
        isSidebarNavCollapse: false,
        
        crumbList: [],
    },
    mutations,
    actions,
    getters,
});
