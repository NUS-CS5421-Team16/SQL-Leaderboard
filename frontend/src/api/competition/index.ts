import axios from "@/utils/request";
export const getCompetitionApi=()=>{
    return axios({
        path:"/competition",
        method:"GET",
    })
}

export const putCompetitionApi=()=>{
    return axios({
        path:"/competition",
        method:"PUT",
    })
}

export const postCompetitionApi=(name:any, description:any, upload_limit:any, concurrent_limit:any,
                                 running_time_limit:any, deadline:any, descendent:any, reference:any, competitorsFileList:any, publicDatasetFileList:any,
                                 privateDatasetFileList:any)=>{
    return axios({
        path:"/competition/",
        method:"POST",
        data: {
            name: name,
            description: description,
            reference_query: reference,
            upload_limit: upload_limit,
            concurrent_limit: concurrent_limit,
            running_time_limit: running_time_limit,
            end_time: deadline,
            descendent_ordering: descendent,
            competitor_info: competitorsFileList,
            public_dataset: publicDatasetFileList,
            private_dataset: privateDatasetFileList
        }
    })
}