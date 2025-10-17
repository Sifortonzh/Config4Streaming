// Bilibili player ad remover - strip ad tags in player manifests/responses
let body = $response.body;
if (!body) $done({});
try {
    let obj = JSON.parse(body);
    if (obj && obj.data) {
        ['ad', 'ads', 'ad_info', 'pre_ad', 'promote'].forEach(f => {
            if (obj.data[f]) delete obj.data[f];
        });
    }
    $done({ body: JSON.stringify(obj) });
} catch(e) { $done({}); }
