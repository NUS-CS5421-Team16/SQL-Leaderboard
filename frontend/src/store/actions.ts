
import permissionList from "@/utils/permission";
import { setDefaultRoute } from "@/utils/recursion-router";

import router, { DynamicRoutes } from "@/router/index";
import view from "@/components/view/view.vue";
function typeOf(obj: any): any {
    const toString: any = Object.prototype.toString;
    const map: any = {
        "[object Boolean]": "boolean",
        "[object Number]": "number",
        "[object String]": "string",
        "[object Function]": "function",
        "[object Array]": "array",
        "[object Date]": "date",
        "[object RegExp]": "regExp",
        "[object Undefined]": "undefined",
        "[object Null]": "null",
        "[object Object]": "object",
    };
    return map[toString.call(obj)];
}
function clone(data: any): any {
    const t = typeOf(data);
    let o: any;

    if (t === "array") {
        o = [];
    } else if (t === "object") {
        o = {};
    } else {
        return data;
    }

    if (t === "array") {
        for (let i = 0; i < data.length; i++) {
            o.push(clone(data[i]));
        }
    } else if (t === "object") {
        for (const i in data) {
            o[i] = clone(data[i]);
        }
    }
    return o;
}
const actions = {
    async FETCH_PERMISSION({ commit }: any) {
        let routes: Array<any> = filterAsyncRouter(permissionList);
        let MainContainer = clone(DynamicRoutes).find(
            (v: any) => v.path === ""
        );
        let children: Array<any> = [];
        children = MainContainer.children;
        children = children.concat(routes);
        commit("SET_MENU", children);
        MainContainer.children = children;
        
        setDefaultRoute([MainContainer]);
        let initialRoutes = router.options.routes;
        router.addRoute(MainContainer);
        commit("SET_PERMISSION", [...initialRoutes]);
    },
};
export const loadView = (view:String) => { 
    return () => import(`@/views/${view}`)
};
function filterAsyncRouter(asyncRouterMap:Array<any>){
    return asyncRouterMap.filter((route:any)=>{
        if(route.children){
            route.component=view;
        }else{
            route.component=loadView(route.component)
        };
        if (route.children != null && route.children && route.children.length) {
            route.children = filterAsyncRouter(route.children)
          } else {
            delete route['children']
            delete route['redirect']
          }
        return true
    });
};

export default actions;
