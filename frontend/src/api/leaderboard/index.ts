import axios from "@/utils/request";

// /competition/rank?private=1&ordering=1
export const getCompetitionRank = (data: any): any => {
    return axios({
        method: "",
        path: "/competition/rank",
        data,
    });
};
