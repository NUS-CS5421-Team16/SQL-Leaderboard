import html2canvas from "./html2canvas.esm.js";
export const canvasEvent=(id:string='',color:string='#fff')=>{
    return new Promise((resolve:any,reject:any)=>{
        html2canvas(document.querySelector(id), {
            useCORS: true,
            taintTest: false,
            logging: true,
            backgroundColor: color,
        }).then((canvas:any) => {
            let url = canvas.toDataURL('image/png');
            resolve(url)
        }).catch(()=>{reject()})
    });
    
}