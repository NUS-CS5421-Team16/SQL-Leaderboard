import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import store from "@/store/index";
//progress
import NProgress from "nprogress";
import "nprogress/nprogress.css";
const routes: Array<RouteRecordRaw> = [
    {
        path: "/login",
        name: "login",
        component: () => import("@/views/login/login.vue"),
    },
    {
        path: "/register",
        name: "register",
        component: () => import("@/views/register/register.vue"),
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

// original
/*router.beforeEach((to: any, from: any, next: any) => {
    NProgress.start();
    if (!window.localStorage.getItem("token") && to.path !== "/login") {
        return next({ path: "/login" });
    };
    if (window.localStorage.getItem("token") && to.path == "/login") return next({ path: "/" });
    if (!store.state.permissionList && to.path != '/login') {
        // router.removeRoute('router');
        return store.dispatch("FETCH_PERMISSION").then(() => {
            next({ ...to, replace: true });
        });
    } else {
        next();
    }
});*/

// edited by ljh
router.beforeEach((to: any, from: any, next: any) => {
    NProgress.start();
    console.log("log1");
    /*if (to.path == "/register") {
        console.log("correct")
        return next({ path: "/register" });
    }

    if (to.path !== "/register" && !window.localStorage.getItem("token") && to.path !== "/login") {
        console.log("problem")
        return next({ path: "/login" });
    };*/

    if (
        window.localStorage.getItem("token") &&
        (to.path == "/login" || to.path == "/register")
    ) {
        console.log("problem2");
        return next({ path: "/" });
    }

    if (
        !store.state.permissionList &&
        to.path != "/login" &&
        to.path != "/register"
    ) {
        // router.removeRoute('router');
        return store.dispatch("FETCH_PERMISSION").then(() => {
            next({ ...to, replace: true });
        });
    } else {
        next();
    }
});

router.afterEach((to: any, from: any, next: any) => {
    NProgress.done();
    try {

        if (to.meta.name) {
            document.title = to.meta.name;
        }
    } catch (err) {}
    let routerList = to.matched;

    store.commit("setCrumbList", routerList);

    store.commit("SET_CURRENT_MENU", to.name);
});

export const DynamicRoutes = [
    {
        path: "",
        component: () => import("@/components/nav/nav.vue"),
        name: "container",
        // redirect: 'home',
        meta: {
            // requiresAuth: true,
            name: "Home",
        },
        children: [
            {
                path: "leaderboard",
                component: () => import("@/views/leaderboard/leaderboard.vue"),
                name: "leaderboard",
                meta: {
                    name: "Leaderboard",
                    icon: "el-icon-house",
                },
            },
            {
                path: "team",
                component: () => import("@/views/team/team.vue"),
                name: "team",
                meta: {
                    name: "Team",
                    icon: "el-icon-user",
                },
            },
            {
                path: "competition-admin",
                component: () => import("@/views/competition/competition.vue"),
                name: "competition-admin",
                meta: {
                    name: "Competition",
                    icon: "el-icon-trophy",
                },
            },
        ],
    },
];

export default router;
