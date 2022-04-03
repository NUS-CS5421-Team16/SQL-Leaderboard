import axios from "@/utils/request";
export const registerApi=(email:any, username:any, password:any)=>{
    return axios({
        path:"/register/",
        method:"POST",
        data: {
            email: email,
            name: username,
            password: password
        }
    })
}