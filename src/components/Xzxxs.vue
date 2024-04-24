<template>
    <div id="main">

    </div>
</template>

<script>
import * as echarts from 'echarts';
export default {
    data(){
        return {
            y_m:["23/11","23/12","24/01","24/02","24/03"],
            zt_cnt:[0,0,0,0,0],
            bt_cnt:[0,0,0,0,0]
        }
    },
    mounted(){
        this.loadData();
    },

    methods: {
    
        loadData(){
            let cnt=0
            let cntb=0
            import('../../../data/07-231101-240331小组学习面试空间预约情况.json')
            .then(module =>{
                
                const months=[11,12,1,2,3]

                var alldata=module.default.data;
                for(let i=0;i<alldata.length;i++){
                    let building=alldata[i][5]
                    let date=new Date(alldata[i][7])
                    let month=date.getMonth()+1
                    if(months.indexOf(month)!=-1){
                        if(building=="闵行校区-包玉刚图书馆"){
                            this.bt_cnt[months.indexOf(month)]++
                        }
                        else if(building=="闵行校区-主馆"){
                            this.zt_cnt[months.indexOf(month)]++
                        }
                        else{
                            console.log("building",building)
                            cntb++
                        }
                    }
                    else{
                        cnt++
                    }
                }
                this.drawGraph()
                console.log("cnt",cnt)
            })

            
            
        },
        drawGraph(){
            
            var myChart = echarts.init(document.getElementById('main'));
            let option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                    type: 'shadow'
                    }
                },
                title: {
                    text: '小组学习室预约次数',
                    left: 'center',
                    textStyle: {
                        color: 'white'
                    }
                },
               
                legend: {
                    data: ['主馆','包玉刚图书馆'],
                    top: '10%',
                    textStyle: {
                        color: 'white'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                    type: 'category',
                    data: this.y_m,
                    axisLabel: {
                        show: true,
                        color: 'white'
                     }
                    }
                ],
                yAxis: [
                    {
                    type: 'value',
                    axisLabel: {
                        show: true,
                        color: 'white'
                     }
                    }
                ],
                series: [
                    {
                    name: '主馆',
                    type: 'bar',
                    stack: '图书馆',
                    emphasis: {
                        focus: 'series'
                    },
                    data: this.zt_cnt,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: 'rgba(102, 153, 255, 0.5)'},
                                {offset: 1, color: 'rgba(102, 153, 255, 0.2)'}
                            ]
                        ),
                        borderRadius: [0, 0, 0, 0]
                    }
                    },
                    {
                    name: '包玉刚图书馆',
                    type: 'bar',
                    stack: '图书馆',
                    emphasis: {
                        focus: 'series'
                    },
                    data: this.bt_cnt,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [
                                {offset: 0, color: 'rgba(153, 255, 51, 0.5)'},
                                {offset: 1, color: 'rgba(153, 255, 51, 0.2)'}
                            ]
                        ),
                        borderRadius: [10, 10, 0, 0]
                    }
                    },
                    
                ]
            };
            myChart.setOption(option);
        }

    }


}
    
</script>

<style>

#main{
    margin-top: 10px;
    width: 100%;
    height: 90%;
}   
</style>