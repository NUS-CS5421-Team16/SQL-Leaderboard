import axios from "@/utils/request";
export const loginApi=(username:any, password:any)=>{
    return axios({
        path:"/login/",
        method:"POST",
        data: {
            email: username,
            password: password
        }
    })
}