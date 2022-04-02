const path = require("path");
function resolve(dir) {
    return path.join(__dirname, dir);
}

module.exports = {
    chainWebpack: config => {
        config.module
            .rule("svg")
            .exclude.add(resolve("src/assets/icons"))
            .end()

        config.module
            .rule("svg-sprite")
            .test(/\.svg$/)
            .include
            .add(resolve("src/assets/icons"))
            .end()
            .use("svg-sprite-loader")
            .loader("svg-sprite-loader")
            .options({
                symbolId: "icon-[name]",
                include: ["src/assets/icons"]
            })
            .end()
            .before("svg-sprite-loader")
            .use("svgo-loader")
            .loader("svgo-loader")
            .options({
                plugins: [
                    { removeAttrs: { attrs: "path:fill" } }
                ]
            })
            .end()
    },
    devServer:{
        open:true,
        proxy: {
            '/api': {
                target: 'http://localhost:8888',
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
    publicPath: '',
    outputDir: '../backend/template/',
    assetsDir: 'static'
}
