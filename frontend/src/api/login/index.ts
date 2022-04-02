import axios from "@/utils/request";

export const loginApi=()=>{
    return axios({
        path:"/users"
    })
}
export const upApi=(data:any)=>{
    return axios({
        path:"/users",
        method:"POST",
        data
    })
}

export const loginApi2=(username:any, password:any)=>{
    return axios({
        path:"/login/",
        method:"POST",
        data: {
            email: username,
            password: password
        }
    })
}