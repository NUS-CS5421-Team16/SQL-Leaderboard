const mutations={
    SET_MENU(state:any, menu:Array<any>) {
        state.sidebarMenu = menu
    },
    SET_PERMISSION(state:any, routes:Array<any>) {
        state.permissionList = routes
    },
    SET_CURRENT_MENU(state:any, currentMenu:string) {
        state.currentMenu = currentMenu
    },
    toggleNavCollapse(state:any) {
        state.isSidebarNavCollapse = !state.isSidebarNavCollapse
    },
    setCrumbList(state:any, list:Array<any>) {
        state.crumbList = list
    },
    setToken(state:any, token:any) {
        state.token = token
    },
    setCid(state:any, cid:any) {
        state.cid = cid
    },
    setRole(state:any, role:any) {
        state.role = role
    },
    setName(state:any, name:any) {
        state.name = name
    },
    setEmail(state:any, email:any) {
        state.email = email
    },
}
export default mutations