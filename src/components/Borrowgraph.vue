<template>
    <div id="box1">
        <div id="lbox">
            <h1 style="color:red;margin:5px">当日借书</h1>
            <h2 v-if="loadFlag" style="color:yellow">{{ dailyBorrowData[fmonth-1][fday-1] }}</h2>
            <h1 style="color:red;margin:5px">当日还书</h1>
            <h2 v-if="loadFlag" style="color:yellow">{{ dailyReturnData[fmonth-1][fday-1] }}</h2>
        </div>
        <div id="rbox">

        </div>
    </div>
    
</template>

<script>
import * as echarts from 'echarts';
export default {
    data(){
        return {
            dailyBorrowData:[],
            dailyReturnData:[],
            loadFlag:false,
            dayNum:[31,28,31,30,31,30,31,31,30,31,30,31]
        }
    },
    props: {
        fday: String,
        fmonth: String,
    },

    watch:{
        fmonth(){
            this.drawGraph(parseInt(this.fmonth))
        }
    },
    mounted(){

        this.loadBorrowData();
        
    },

    methods: {
        loadBorrowData(){

            for(var month=0;month<12;month++){
                this.dailyBorrowData.push([])
                this.dailyReturnData.push([])
                for(var day=0;day<this.dayNum[month];day++){
                    this.dailyBorrowData[this.dailyBorrowData.length-1].push(0)
                    this.dailyReturnData[this.dailyReturnData.length-1].push(0)
                }
            }
            
            import('../../../data/01-2023年全年图书借阅预约归还等数据-更新.json')
            .then(module => {
                // 模块加载成功，module 包含 JSON 文件的默认导出内容
                var alldata=module.default.RECORDS;
                for(var i=0;i<alldata.length;i++){
                    var etype=alldata[i].事件类型
                    var time=parseInt(alldata[i].发生时间).toString()
                    var month=parseInt(time.substring(4,6))-1
                    var day=parseInt(time.substring(6,8))-1
                   
                    if(month<0 || month>11|| day<0|| (day >this.dayNum[month]-1)){
                        
                    }
                    else{
                        //忽略续借数据
                        if(etype=="借阅"){
                            this.dailyBorrowData[month][day]++
                            
                        }
                        else if(etype=="归还"){
                            this.dailyReturnData[month][day]++
    
                        }
                    }   
                }
                this.loadFlag=true
                this.drawGraph(1)
            })
            .catch(error => {
                // 模块加载失败，处理错误
                console.error('Error loading JSON file:', error);
                console.log(this.dailyBorrowData)
            });
            
        },

        drawGraph(m){
            // 初始化 ECharts 实例
            if(!this.loadFlag){
                return
            }
            
            
            let myChart = echarts.init(document.getElementById('rbox'));
            let xdata=[];
            for(let i=1;i<=this.dayNum[m-1];i++){
                xdata.push(i.toString())
            }
           
            
            // 配置项
            let option = {
                title: {
                    text: m+'月借还书趋势',
                    left: 'center',
                    textStyle: {
                        color: 'red'
                    }
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['借阅','归还'],
                    top: '10%'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: xdata,
                    axisLabel: {
                        show: true,
                        textStyle: {
                        color: 'red'
                        }
                     }
                }, 
                yAxis: {
                    type: 'value',
                    axisLabel: {
                    show: true,
                        textStyle: {
                        color: 'red'
                        }
                    }
                },
                series: [
                    {
                        name: '借阅',
                        type: 'line',
                        data: this.dailyBorrowData[m-1],
                        smooth: true,
                        areaStyle: {
                            color: 'rgba(255, 0, 0, 0.5)' // 设置曲线下的面积颜色为半透明红色
                        }
                    },
                    {
                        name: '归还',
                        type: 'line',
                        data: this.dailyReturnData[m-1],
                        smooth: true,
                        areaStyle: {
                            color: 'rgba(0, 0, 255, 0.5)' // 设置曲线下的面积颜色为半透明蓝色
                        }
                    }
                   
                ]
            };
            
            // 使用刚指定的配置项和数据显示图表
            myChart.setOption(option);
        }
    }
}
</script>

<style>

#day{
    width: 30%;
    height: 80%;
}

#month{
    width: 70%;
    height: 80%;
}

#box1{
    display: flex;
    width: 100%;
    height: 80%
}
#lbox{
    width:30%;
    height: 100%
}
#rbox{
    width:60%;
    height: 100%
}
</style>