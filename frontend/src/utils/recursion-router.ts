/**
 *
 * @param  {Array} userRouter 
 * @param  {Array} allRouter  
 * @return {Array} realRoutes 
 */

 export function recursionRouter(userRouter:any[] = [], allRouter:any = []) {
    // console.log(userRouter,allRouter,1)
    var realRoutes:any[] = []
    allRouter.forEach((v:any, i:number) => {
        userRouter.forEach((item:any, index:number) => {
            if (item.type === v.type) {
                if (item.children && item.children.length > 0) {
                    v.children = recursionRouter(item.children, v.children)
                }
                realRoutes.push(v)
            }
        })
    })
    // console.log(realRoutes,2)
    return realRoutes
}

/**
 *
 * @param {Array} routes 
 *
 */
export function setDefaultRoute(routes:any[]) {
    routes.forEach((v:any, i:number) => {
        if (v.children && v.children.length > 0) {
            v.redirect = { name: v.children[0].name }
            setDefaultRoute(v.children)
        }
    })
}
