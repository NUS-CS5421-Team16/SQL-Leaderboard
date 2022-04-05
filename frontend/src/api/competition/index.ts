import axios from "@/utils/request";
export const getCompetitionApi=()=>{
    return axios({
        path:"/competition/",
        method:"GET",
    })
}

export const hasCompetitionApi=()=>{
    return axios({
        path:"/competition/has_competition/",
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