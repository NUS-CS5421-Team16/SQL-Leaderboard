import axios from "@/utils/request";
export const getCompetitionApi=()=>{
    return axios({
        path:"/competition/",
        method:"GET",
    })
}

export const putCompetitionApi=(data:FormData)=>{
    return axios({
        path:"/competition/",
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