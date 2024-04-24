<template>
    <div id="officeChart" style="width: 100%; height: 90%;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { color } from 'echarts';

export default {
    
    //需获得的：每间办公室当月预约总数
    data(){
        return {
            like:1705405200000,
            data2:[],
            data16:[],
            data21:[],
            buildings:[],
            starts:[],
            ends:[],
        }
    },
    mounted(){
        this.loadOfficeData();
    },

    methods: {
        timestampToMonth(timestamp) {
            timestamp = timestamp ? timestamp : null;
            var A={}
             var date = new Date(timestamp);
             let Y = date.getFullYear().toString().substring(2,4)+'/'
            let M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) ;            
            
            return Y+M;
        },

        loadOfficeData(){
            import('../../../data/06-2021年11月-2024年4月共享办公位预约情况.json')
            .then(module =>{
                const rooms=['522-A','523-A','523-B','523-C','523-D','523-E','523-F','523-G']
                const months=["23/08","23/09","23/10","23/11","23/12","24/01","24/02","24/03","24/04"]

                var alldata=module.default.data;
                var cs=[]
                var ce=[]
                let mapData=[]
                for(let i=0;i<months.length;i++){
                    for(let j=0;j<rooms.length;j++){
                        mapData.push([i,j,0])
                    }
                }
                for(var i=0;i<alldata.length;i++){
                    
                    var month=this.timestampToMonth(alldata[i][0]);
                    if(months.indexOf(month)!=-1){
                        mapData[rooms.indexOf(alldata[i][3])+8*months.indexOf(month)][2]++;
                    }
                    else{
                        
                    }
                }
                console.log(mapData)
                this.showChart(mapData)
            })
        
            
        },

        showChart(data){
            // prettier-ignore
            let Chart = echarts.init(document.getElementById('officeChart'));

            const rooms=['522-A','523-A','523-B','523-C','523-D','523-E','523-F','523-G']
            const months=["23/08","23/09","23/10","23/11","23/12","24/01","24/02","24/03","24/04"]
           
            var option = {
            tooltip: {
                position: 'top'
            },
            grid: {
                left: '20%',
                height: '65%',
                top: '10%'
            },
            xAxis: {
                type: 'category',
                data: months,
                splitArea: {
                show: true
                },
                axisLabel: {
                    show: true,
                    textStyle: {
                    color: 'white'
                    }
                }
            },
            yAxis: {
                type: 'category',
                data: rooms,
                splitArea: {
                show: true
                },
                axisLabel: {
                    show: true,
                    textStyle: {
                    color: 'white'
                    }
                }
            },
            visualMap: {
                min: 0,
                max: 100,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '0%',
                inRange: {
                color: ['rgba(204, 255, 102, 0.0)', 'rgba(0, 51, 102, 1)']
                },
            },
            series: [
                {
                name: '单月预约次数',
                type: 'heatmap',
                data: data,
                label: {
                    show: true,
                },
                emphasis: {
                    itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
                }
            ]
            };
            Chart.setOption(option);
        }

    }
}
</script>

<style>
</style>