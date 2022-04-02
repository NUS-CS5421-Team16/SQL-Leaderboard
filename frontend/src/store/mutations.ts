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
    }
}
export default mutations