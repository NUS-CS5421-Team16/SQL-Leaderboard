// import Vue from 'vue'
import axiosNew from 'axios';
import {config} from '@/utils/config'
import store from "@/store";
import router from "@/router";
axiosNew.defaults.timeout =30000;
import { ElMessage, ElMessageBox } from 'element-plus'

axiosNew.interceptors.request.use(
    config => {
        //config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
        if (sessionStorage.getItem('token') == null && !config.url.includes('/register/')) {
            router.push({path:"/login"});
        }
        if (config.url?.includes("/competition/") && (config.method == "post")) {
            config.headers['Content-Type'] = 'multipart/form-data';
        }
        if (config.url?.includes("/competition/") && (config.method == "put")) {
            config.headers['Content-Type'] = 'multipart/form-data';
        }
        if (config.url?.includes("/competitor/") && (config.method == "put")) {
            config.headers['Content-Type'] = 'multipart/form-data';
        }
        if (!config.url.includes("/register/") && !config.url.includes("/login/") && sessionStorage.getItem('token') != "") {
            let token = "Token " + sessionStorage.getItem('token')
            config.headers.Authorization = token
        }
        /*if (token) {
            config.headers.common['token'] =token
        }*/
        //config.headers['Authorization'] = token
        return config
    },
    err => {
        return Promise.reject(err);
    }

)

axiosNew.interceptors.response.use(response => {
        try{
            let token = response?.data?.token;
            // store info from login response
            if(token != null){
                sessionStorage.setItem('token', token)
                sessionStorage.setItem('cid', response.data.id)
                sessionStorage.setItem('email', response.data.email)
                sessionStorage.setItem('name', response.data.name)
                sessionStorage.setItem('role', response.data.role)
                store.commit('setToken', token)
                if (response.data.id != null) {
                    store.commit('setCid', response.data.id)
                }
                if (response.data.email != null) {
                    store.commit('setEmail', response.data.email)
                }
                if (response.data.name != null) {
                    store.commit('setName', response.data.name)
                }
                if (response.data.role != null) {
                    store.commit('setRole', response.data.role)
                }
            }
        }catch(err){
            console.log("Don't need to get token for this response",err)
        };

        /*if(response.data.code==10001||response.data.code==402){// token expired or is null, jump to login
            store.dispatch('tokenChange',"");
            router.push({path:"/login"});

        }*/
        //console.log("the token is " + store.getters.getToken)
        return response;
    }
    ,err=>{
        return Promise.reject(err)
    }
);
// axiosNew.defaults.baseURL=""
const axios=function({path,method="GET",data={}}:any={}){
    return new Promise((resolve,reject)=>{
        let datas:object={params:{...data}}
        datas={...{data}};
        axiosNew({
            url:`${config.host}${path}`,
            method,
            ...datas
        }).then(res=>{
            resolve(res.data)
        }).catch(err=>{
            const status = `${err.response.status}`;
            const prefix = status[0];
            if (prefix === "4" || prefix === "5") {
                const data = err.response.data;
                let str: string = "";
                if (
                    Object.prototype.toString.call(data) ===
                    "[object String]"
                ) {
                    str = `HTTP status code: ${status}`;
                } else if (data.hasOwnProperty("message")) {
                    str = data.message;
                } else {
                    str = JSON.stringify(data);
                }
                ElMessageBox.alert(str, "Error msg", {
                    confirmButtonText: "OK",
                });
            }
            resolve(-1)
        })
    })
};
export default axios



