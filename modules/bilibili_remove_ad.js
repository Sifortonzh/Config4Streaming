// Bilibili JSON ad remover (deep clean)
let body = $response.body;
if (!body) $done({});
try {
    let obj = JSON.parse(body);
    function deepClean(o) {
        if (!o || typeof o !== 'object') return;
        for (let k of Object.keys(o)) {
            try {
                if (/ad|banner|advert|promote|promotions|recommend|roll|follow/i.test(k)) {
                    delete o[k];
                } else {
                    deepClean(o[k]);
                }
            } catch(e){}
        }
    }
    deepClean(obj);
    $done({ body: JSON.stringify(obj) });
} catch (e) {
    $done({});
}
