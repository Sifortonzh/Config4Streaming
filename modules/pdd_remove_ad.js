// Pinduoduo ad cleaner
let body = $response.body;
if(!body) $done({});
try{
    let obj = JSON.parse(body);
    function clean(o){
        if(!o||typeof o!=='object') return;
        for(let k of Object.keys(o)){
            try{
                if(/ad|promotion|recommend|coupon|banner/i.test(k)){
                    delete o[k];
                }else{
                    clean(o[k]);
                }
            }catch(e){}
        }
    }
    clean(obj);
    $done({ body: JSON.stringify(obj) });
}catch(e){ $done({}); }
