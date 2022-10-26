
//値をグラフに表示させる
// Chart.plugins.register({
//     afterDatasetsDraw: function (chart, easing) {
//         var ctx = chart.ctx;

//         chart.data.datasets.forEach(function (dataset, i) {
//             var meta = chart.getDatasetMeta(i);
//             if (!meta.hidden) {
//                 meta.data.forEach(function (element, index) {
//                     // 値の表示
//                     ctx.fillStyle = 'rgb(0, 0, 0,0.8)';//文字の色
//                     var fontSize = 12;//フォントサイズ
//                     var fontStyle = 'normal';//フォントスタイル
//                     var fontFamily = 'Arial';//フォントファミリー
//                     ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);

//                     var dataString = ""+dataset.data[index]

//                     // 値の位置
//                     ctx.textAlign = 'center';//テキストを中央寄せ
//                     ctx.textBaseline = 'middle';//テキストベースラインの位置を中央揃え

//                     var padding = 5;//余白
//                     var position = element.tooltipPosition();
//                     ctx.fillText(dataString, position.x, position.y - (fontSize / 2) - padding);
    
//                 });
//             }
//         });
//     }
// });


function days_langs(json){
    return fetch(json)
    .then( res => res.json())
    .then( myjson => {
        let days = []
        let names = []
        let langs = new Array(19)
        for (let i = 0; i < 19; i++) {
            langs[i] = new Array(1)
        }
        odd = 0
        for (const key in myjson) {
            if (odd++%2 == 1) continue
            days.push(key)
            count = 0
            var pairs = Object.entries(myjson[key]);
            pairs.sort(function(p1, p2){
                var p1Key = p1[0], p2Key = p2[0];
                if(p1Key < p2Key){ return -1; }
                if(p1Key > p2Key){ return 1; }
                return 0;
            })
            myjson[key] = Object.fromEntries(pairs);
            for (const vkey in myjson[key]) {
                langs[count++].push(myjson[key][vkey])
            }
        }
        for (const key in myjson) {
            for (const vkey in myjson[key]) {
                names.push(vkey)
            }
            break
        }
        return {days, langs, names}
    }).catch( error => {
        console.log("エラ-", error);
    });
}
//=========== 折れ線グラフ（複数） ============//
$('#chart02').on('inview', function(event, isInView) {//画面上に入ったらグラフを描画
    if (isInView) {
        var json = document.getElementById('json_link').title;
        const dls = days_langs(json)
        const promise = new Promise((resolve, reject) => {
            if ('処理が成功') {
                resolve(dls);
            } else {
                reject(new Error('error'));
            }
        });
        promise.then((value) => {
            var ctx=document.getElementById("chart02");//グラフを描画したい場所のid
            var chart=new Chart(ctx,{
                type:'line',//グラフのタイプ
                data:{//グラフのデータ
                    labels: value["days"],//データの名前
                    datasets: [
                            {
                        label:value["names"][0],//グラフのタイトル
                        borderColor:    "rgba(255,0,0,1)",//グラフの線の色
                        backgroundColor:"rgba(255,0,0,0)",//グラフの背景色透過
                        data: value["langs"][0]//横列に並ぶデータ
                            },{
                        label:value["names"][1],//グラフのタイトル
                        borderColor:    "rgba(130,201,169,0.5)",//グラフの線の色
                        backgroundColor:"rgba(130,201,169,0)",//グラフの背景色透過
                        data: value["langs"][1]//横列に並ぶデータ
                            },{
                        label:value["names"][2],//グラフのタイトル
                        borderColor:    "rgba(255,183,76,0.5)",//グラフの線の色
                        backgroundColor:"rgba(255,183,76,0)",//グラフの背景色透過
                        data: value["langs"][2]//横列に並ぶデータ
                            },{
                        label:value["names"][3],//グラフのタイトル
                        borderColor:    "rgba(5,13,6,0.5)",//グラフの線の色
                        backgroundColor:"rgba(5,13,6,0)",//グラフの背景色透過
                        data: value["langs"][3]//横列に並ぶデータ
                            },{
                        label:value["names"][4],//グラフのタイトル
                        borderColor:    "rgba(200,253,0,0.5)",//グラフの線の色
                        backgroundColor:"rgba(200,253,0,0)",//グラフの背景色透過
                        data: value["langs"][4]//横列に並ぶデータ
                            },{
                        label:value["names"][5],//グラフのタイトル
                        borderColor:    "rgba(35,93,156,0.5)",//グラフの線の色
                        backgroundColor:"rgba(35,93,156,0)",//グラフの背景色透過
                        data: value["langs"][5]//横列に並ぶデータ
                            },{
                        label:value["names"][6],//グラフのタイトル
                        borderColor:    "rgba(105,0,6,0.5)",//グラフの線の色
                        backgroundColor:"rgba(105,0,6,0)",//グラフの背景色透過
                        data: value["langs"][6]//横列に並ぶデータ
                            },{
                        label:value["names"][7],//グラフのタイトル
                        borderColor: "rgba(55,53,76,0.5)",//グラフの線の色
                        backgroundColor:"rgba(55,53,76,0)",//グラフの背景色透過
                        data: value["langs"][7]//横列に並ぶデータ
                            },{
                        label:value["names"][8],//グラフのタイトル
                        borderColor: "rgba(25,13,176,0.5)",//グラフの線の色
                        backgroundColor:"rgba(25,13,176,0)",//グラフの背景色透過
                        data: value["langs"][8]//横列に並ぶデータ
                            },{
                        label:value["names"][9],//グラフのタイトル
                        borderColor:    "rgba(25,183,256,0.5)",//グラフの線の色
                        backgroundColor:"rgba(25,183,256,0)",//グラフの背景色透過
                        data: value["langs"][9]//横列に並ぶデータ
                            },{
                        label:value["names"][10],//グラフのタイトル
                        borderColor:    "rgba(0,243,76,0.5)",//グラフの線の色
                        backgroundColor:"rgba(0,243,76,0)",//グラフの背景色透過
                        data: value["langs"][10]//横列に並ぶデータ
                            },{
                        label:value["names"][11],//グラフのタイトル
                        borderColor:    "rgba(185,183,176,0.5)",//グラフの線の色
                        backgroundColor:"rgba(185,183,176,0)",//グラフの背景色透過
                        data: value["langs"][11]//横列に並ぶデータ
                            },{
                        label:value["names"][12],//グラフのタイトル
                        borderColor:    "rgba(25,183,176,0.5)",//グラフの線の色
                        backgroundColor:"rgba(25,183,176,0)",//グラフの背景色透過
                        data: value["langs"][12]//横列に並ぶデータ
                            },{
                        label:value["names"][13],//グラフのタイトル
                        borderColor:    "rgba(55,19,26,0.5)",//グラフの線の色
                        backgroundColor:"rgba(55,19,26,0)",//グラフの背景色透過
                        data: value["langs"][13]//横列に並ぶデータ
                            },{
                        label:value["names"][14],//グラフのタイトル
                        borderColor:    "rgba(25,13,76,0.5)",//グラフの線の色
                        backgroundColor:"rgba(25,13,76,0)",//グラフの背景色透過
                        data: value["langs"][14]//横列に並ぶデータ
                            },{
                        label:value["names"][15],//グラフのタイトル
                        borderColor:    "rgba(125,253,176,0.5)",//グラフの線の色
                        backgroundColor:"rgba(125,253,176,0)",//グラフの背景色透過
                        data: value["langs"][15]//横列に並ぶデータ
                            },{
                        label:value["names"][16],//グラフのタイトル
                        borderColor:    "rgba(25,183,176,0.5)",//グラフの線の色
                        backgroundColor:"rgba(25,183,176,0)",//グラフの背景色透過
                        data: value["langs"][16]//横列に並ぶデータ
                            },{
                        label:value["names"][17],//グラフのタイトル
                        borderColor:    "rgba(25,183,76,1)",//グラフの線の色
                        backgroundColor:"rgba(25,183,76,0)",//グラフの背景色透過
                        data: value["langs"][17]//横列に並ぶデータ
                            },{
                        label:value["names"][18],//グラフのタイトル
                        borderColor:    "rgba(25,83,76,0.5)",//グラフの線の色
                        backgroundColor:"rgba(25,83,76,0)",//グラフの背景色透過
                        data: value["langs"][18]//横列に並ぶデータ
                            }
                        ]
                },
                options:{//グラフのオプション
                    responsive: true,
                    legend:{
                        display: true//グラフの説明を表示
                    },
                    tooltips:{//グラフへカーソルを合わせた際のツールチップ詳細表示の設定
                        callbacks:{
                                label: function(tooltipItems, data) {
                                    if(tooltipItems.yLabel == "0"){
                                        return "";
                                    }
                                    return data.datasets[tooltipItems.datasetIndex].label + "：" + tooltipItems.yLabel + "";//Kgを最後につける
                                }
                            }
                    },
                    title:{//上部タイトル表示の設定
                        display: true,
                        fontSize:10,
                        text: '単位：求人数'
                    },
                    scales:{
                        yAxes:[//グラフ縦軸（Y軸）設定
                            {
                                ticks:{
                                    beginAtZero:true,//0からスタート
                                    suggestedMax: 12000,//最大が100
                                    suggestedMin: 0,//最小が0
                                    stepSize: 2000,//10づつ数値が刻まれる
                                    callback: function(value){
                                        return  value +  ''//数字＋%で表示      
                                    }
                                }
                            }
                        ],
                        xAxes:[//棒グラフ横（X軸）設定
                            {
                                barPercentage:0.5,//バーの太さ
                            }
                        ]
                    }
                }
            });
            }, (error) => {
            console.error("error:", error.message);
        });
        // daysに日時のデータ
        // langsに言語ごとのデータ

    }
});