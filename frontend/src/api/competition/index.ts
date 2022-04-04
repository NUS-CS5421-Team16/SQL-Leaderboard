import axios from "@/utils/request";
export const getCompetitionApi=()=>{
    return axios({
        path:"/competition/",
        method:"GET",
    })
}

export const putCompetitionApi=(data:FormData, cid)=>{
    console.log("api: " + data)
    return axios({
        path:"/competition/" + cid + "/",
        method:"PUT",
        data: data
    })
}

export const postCompetitionApi=(data:FormData)=>{
    return axios({
        path:"/competition/",
        method:"POST",
        data: data
    })
}

export const getPublic=()=>{
    return axios({
        path:"/competition/download_public/",
        method:"GET",
    })
}

export const getReference=()=>{
    return axios({
        path:"/competition/download_reference/",
        method:"GET",
    })
}