// import Vue from 'vue'
import axiosNew from 'axios';
import {config} from '@/utils/config'
import store from "@/store";
import router from "@/router";
axiosNew.defaults.timeout =3000;

axiosNew.interceptors.request.use(
    config => {

        return config
    },

    err => {
        return Promise.reject(err);
    }

)

axiosNew.interceptors.response.use(response => {

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



