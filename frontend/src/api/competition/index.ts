import axios from "@/utils/request";
export const getCompetitionApi=()=>{
    return axios({
        path:"/competition/",
        method:"GET",
    })
}

export const putCompetitionApi=(name:any, description:any, upload_limit:any, concurrent_limit:any,
                                running_time_limit:any, deadline:any, descendent:any, files:FormData)=>{
    return axios({
        path:"/competition/",
        method:"PUT",
        data: {
            name: name,
            description: description,
            reference_query: files.get("reference_query"),
            upload_limit: upload_limit,
            concurrent_limit: concurrent_limit,
            running_time_limit: running_time_limit,
            end_time: deadline,
            descendent_ordering: descendent,
            competitor_info: files.get("competitor_info"),
            public_sql: files.get("public_sql"),
            private_sql: files.get("private_sql")
        },
        headers: {
            'Content-Type': 'multipart/form-data;'
        }
    })
}

/*export const postCompetitionApi=(name:any, description:any, upload_limit:any, concurrent_limit:any,
                                 running_time_limit:any, deadline:any, descendent:any, files:FormData)=>{
    return axios({
        path:"/competition/",
        method:"POST",
        data: {
            name: name,
            description: description,
            reference_query: files.get("reference_query"),
            upload_limit: upload_limit,
            concurrent_limit: concurrent_limit,
            running_time_limit: running_time_limit,
            end_time: deadline,
            descendent_ordering: descendent,
            competitor_info: files.get("competitor_info"),
            public_sql: files.get("public_sql"),
            private_sql: files.get("private_sql")
        },
        headers: {
            'Content-Type': 'multipart/form-data;'
        }
    })
}*/

export const postCompetitionApi=(data:FormData)=>{
    return axios({
        path:"/competition/",
        method:"POST",
        data: data
    })
}