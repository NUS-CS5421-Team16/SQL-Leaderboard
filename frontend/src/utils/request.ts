// import Vue from 'vue'
import axiosNew from 'axios';
import {config} from '@/utils/config'
import store from "@/store";
import router from "@/router";
axiosNew.defaults.timeout =30000;

axiosNew.interceptors.request.use(
    config => {
        //config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
        //let token =sessionStorage.getItem('token');
        console.log("url: " + config.url)
        console.log("intercept")
        console.log("ends with " + config.url?.endsWith("/competition/"))
        console.log("method " + config.method)
        if (config.url?.endsWith("/competition/") && config.method == "post") {
            console.log("success")
            config.headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryn8D9asOnAnEU4Js0';
        }
        if (store.getters.getToken != "") {
            let token = "Token " + store.getters.getToken
            console.log("token: " + token)
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
            let token = response.data.token;
            // store info from login response
            if(token != null){
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
        if(method==="POST") datas={...{data}};
        axiosNew({
            url:`${config.host}${path}`,
            method,
            ...datas
        }).then(res=>{
            resolve(res.data)
        }).catch(err=>{resolve(-1)})
    })
};
export default axios



