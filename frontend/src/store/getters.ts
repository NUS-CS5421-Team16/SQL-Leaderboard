const getters={
    GET_MENU:(state:any)=>state.sidebarMenu,
    GET_CURRENTMENU:(state:any)=>state.currentMenu,
    getCrumbList:(state:any)=>state.crumbList,
    getIsSidebarNavCollapse:(state:any)=>state.isSidebarNavCollapse,
    getToken:(state:any)=>state.token,
    getCid:(state:any)=>state.cid,
    getRole:(state:any)=>state.role,
    getName:(state:any)=>state.name,
    getEmail:(state:any)=>state.email,
}
export default getters