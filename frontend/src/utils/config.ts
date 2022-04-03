console.log("NODE_ENV", process.env.NODE_ENV);
/**
 * process.env.NODE_ENV
 * development
 * production
 */


// when we choose to build, NODE_ENV = production and use http://localhost:8000.


/**
 * when frontend choose to npm run dev, frontend's port is 8080. Backend's port is 8000. Hence CORS. 
 * So we use /api. In vue.config.js, devServer can proxy to backend's localhost:8000.
*/
const host =
    process.env.NODE_ENV === "production" ? "http://localhost:8000" : "/api";
export const config = {
    host,
};
