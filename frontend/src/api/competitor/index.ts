import axios from "@/utils/request";

// Update Team
export const updateTeam = (cid: string, data: FormData) => {
  console.log(data)
  return axios({
    method: "PUT",
    path: `/competitor/${cid}/team/`,
    data,
  });
};

// Get comprtitor
export const getCompetitor = (cid: string) => {
  return axios({
    method: "GET",
    path: `/competitor/${cid}/`,
  });
};

// // Uplaod SQL
// export const uploadFile = (cid: string, data: any) => {
//   return axios({
//     method: "POST",
//     path: `/competitor/${cid}/task`,
//     data,
//   });
// };
