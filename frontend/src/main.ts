import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./styles/index.scss";
import "@/styles/color/index.scss";
import ElementPlus from "element-plus";
import "element-plus/lib/theme-chalk/index.css";
import { createI18n } from "vue-i18n";
import messages from "@/utils/language";
// import "@/components/svg/svg";
// import icons from "@/components/svg/svg.vue";
import 'xe-utils'
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
const i18n = createI18n({
    locale: "en-US", 
    messages,
});
function useTable (app: any) {
    app.use(VXETable)

    // app.config.globalProperties.$XModal = VXETable.modal
    // app.config.globalProperties.$XPrint = VXETable.print
    // app.config.globalProperties.$XSaveFile = VXETable.saveFile
    // app.config.globalProperties.$XReadFile = VXETable.readFile
  }

createApp(App)
    .use(store)
    .use(router)
    .use(ElementPlus)
    .use(i18n)
    .use(useTable)
    // .component('icons',icons)
    .mount("#app")
//     const app=createApp(App);
// app.component('icons', icons) 