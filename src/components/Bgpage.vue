<template>
    <div class="bgpage">
        <Header></Header>
        <div>
            <div class="container">
                <div class="box">
                    <Viewbox
                        title="检索热度"
                        :boxb="true"
                    >
                        <div class="word-cloud">
                            <div v-for="(item, index) in heatData" :key="index" :style="{ fontSize: item[1] + 'px', left: Math.random() * 75 + '%', top: Math.random() * 60 + '%' }">{{ item[0] }} </div>
                        </div>
                    </Viewbox>
                </div>
                <div class="box">
                    <!-- 月份和日期输入框 -->
                    <div>
                        月份：<input type="text" v-model="month" @input="updateDataStr">
                        日期：<input type="text" v-model="day" @input="updateDataStr"><br>
                    </div>
                    <Viewbox
                        title="1月1日实时在馆人数分布"
                        :boxb="true"
                    >
                        <!-- 曲线图容器 -->
                        <div id="attendanceChart" style="width: 100%; height: 100%;"></div>
                    </Viewbox>
                </div>
                <div class="box">
                    <Viewbox
                        :title="subTitle"
                        :boxb="true"
                    />   
                </div>
            </div>
            <div class="container">
                <div class="box">
                    <Viewbox
                        title="用户画像"
                        :boxb="true"
                    >
                        <div id="portrait" style="width: 100%; height: 100%;"></div>
                    </Viewbox>
                </div>
                <div class="box">
                    <Viewbox
                        title="读者学院分布"
                        :boxb="true"
                    >
                        <div id="department" style="width: 100%; height: 100%;"></div>
                    </Viewbox>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Header from './Header.vue'
import Viewbox from './viewbox/Viewbox.vue'
import * as echarts from 'echarts';

export default {
    components: {
        Header,
        Viewbox
    },
    data() {
        return {
            subTitle: "子标题",
            heatData: [], // 保存检索热度数据
            entryData: [], // 保存入馆数据
            // groupedData: {本科: 1002523, 博士: 334600, 其他: 1158997, 研究生: 628196, 教师: 128236}, // 保存按 ID 分组的入馆数据
            groupedData: {},
            academyNumberData: {},    // 入馆人数
            academyBorrowData: {},
            libraryAttendanceData: [], // 新建全年在馆人数数据
            month: '1', // 默认月份为1
            day: '11', // 默认日期为1
        }
    },
    mounted() {
        // Load the heat data when the component is mounted
        this.loadHeatData();
        // Load the library attendance data when the component is mounted
        this.loadLibraryAttendanceData();
        this.loadEntryData();   // 数据量巨大，最好预处理，直接使用line #72 的数据进行绘制，而不是实时处理，延时高达1min
        // this.drawPortrait();
        // this.loadBorrowData();
        // this.drawDepartment();
    },
    methods: {
        loadHeatData() {
            // Load the JSON data asynchronously
            import('/data/03-检索热度.json')
                .then(module => {
                    // Once data is loaded, assign it to the heatData array
                    this.heatData = module.default.data;
                })
                .catch(error => {
                    console.error('Error loading heat data:', error);
                });
                console.log(this.heatData);
        },
        loadLibraryAttendanceData() {
            // Load the JSON data asynchro nously
            let dateStr = `2023/${this.month}/${this.day}`;
            import('/data/05-2023年全年实时在馆人数-2分钟一更新.json')
                .then(module => {
                    // Filter the data for January 1st
                    this.libraryAttendanceData = module.RECORDS.filter(item => item.logTime.startsWith(dateStr));
                    

                    this.drawAttendanceChart();
                })
                .catch(error => {
                    console.error('Error loading library attendance data:', error);
                });
        },
        updateDataStr() {
            this.dateStr = `2023/${this.month}/${this.day}`;
            this.loadLibraryAttendanceData();
        },
        drawAttendanceChart() {
            // 初始化 ECharts 实例
            let attendanceChart = echarts.init(document.getElementById('attendanceChart'));
            
            // 准备数据
            let timeData = this.libraryAttendanceData.map(item => {
                // 找到空格，并取空格之后的部分
                return item.logTime.split(' ')[1];
            }); // 提取时间部分
            let zgData = this.libraryAttendanceData.map(item => item.zg);
            let lzdData = this.libraryAttendanceData.map(item => item.lzd);
            let bygData = this.libraryAttendanceData.map(item => item.byg);
            let xhskgData = this.libraryAttendanceData.map(item => item.xhskg);
            
            // 配置项
            let option = {
                title: {
                    text: '1月1日实时在馆人数分布',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['主馆', '李政道图书馆', '包玉刚图书馆', '徐汇社科阅览室']
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
                    data: timeData,
                    axisLabel: {
                        formatter: function (value, index) {
                            // 只显示部分时间刻度
                            if (index % 6 === 0) {
                                return value;
                            } else {
                                return '';
                            }
                        }
                    }
                }, 
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '主馆',
                        type: 'line',
                        data: zgData,
                        smooth: true,
                        areaStyle: {
                            color: 'rgba(255, 0, 0, 0.5)' // 设置曲线下的面积颜色为半透明红色
                        }
                    },
                    {
                        name: '李政道图书馆',
                        type: 'line',
                        data: lzdData,
                        smooth: true,
                        areaStyle: {
                            color: 'rgba(0, 0, 255, 0.5)' // 设置曲线下的面积颜色为半透明蓝色
                        }
                    },
                    {
                        name: '包玉刚图书馆',
                        type: 'line',
                        data: bygData,
                        smooth: true,
                        areaStyle: {
                            color: 'rgba(0, 255, 0, 0.5)' // 设置曲线下的面积颜色为半透明绿色
                        }
                    },
                    {
                        name: '徐汇社科阅览室',
                        type: 'line',
                        data: xhskgData,
                        smooth: true,
                        areaStyle: {
                            color: 'rgba(255, 165, 0, 0.5)' // 设置曲线下的面积颜色为半透明橙色
                        }
                    }
                ]
            };
            
            // 使用刚指定的配置项和数据显示图表
            attendanceChart.setOption(option);
        },
        loadEntryData() {
            // 如果没有id，默认为其他
            // ! 我将文件名修改成02了，直接修改成本地的即可
            fetch('/data/02.json')
                .then(response => response.json())
                .then(data => {
                    this.entryData = data.RECORDS;
                    this.groupDataByID(this.entryData);
                })
                .catch(error => {
                    console.error('Error loading entry data:', error);
                });
            // console.log(this.heatData);
            // console.log(this.entryData);
        },
        groupDataByID(data) {
            data.forEach(element => {
                let id = element.ID_type;
                let academy = element.Department;
                if (id === '' || id === null) {
                    id = '其他';
                }
                if (!this.groupedData[id]) {
                    this.groupedData[id] = 1;
                } else {
                    this.groupedData[id] += 1;
                }
                if (academy !== '' && academy !== null) {
                    if (!this.academyNumberData[academy]) {
                        this.academyNumberData[academy] = 1;
                    } else {
                        this.academyNumberData[academy] += 1;
                    }
                }
                
            });
            this.drawPortrait();
            this.loadBorrowData();
            console.log(this.groupedData);
        },
        drawPortrait() {
            var chartDom = document.getElementById('portrait');
            var myChart = echarts.init(chartDom);
            let option = {
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        top: '5%',
                        left: 'left',
                        orient: 'vertical',
                        formatter: function (name) {
                            var target = myChart.getOption().series[0].data.find((item) => {return item.name === name});
                            return name + ' : ' + target.value;
                        }
                    },
                    series: [
                        {
                        name: 'Access From',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        padAngle: 5,
                        itemStyle: {
                            borderRadius: 10
                        },
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                            show: true,
                            fontSize: 40,
                            fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: Object.entries(this.groupedData).map(([key, value]) => ({value : value, name : key}))
                        }
                    ]
                };
            myChart.setOption(option);
        },
        loadBorrowData() {
            fetch('/data/01.json')
                .then(response => response.json())
                .then(data => {
                    this.groupDataByDepartment(data.RECORDS);
                })
                .catch(error => {
                    console.error('Error loading entry data:', error);
                });
        },
        groupDataByDepartment(data) {
            data.forEach(element => {
                let dp = element["学院"]
                let type = element["事件类型"]
                if (dp !== '' && dp !== null && type === "借阅") {
                    if (!this.academyBorrowData[dp]) {
                        this.academyBorrowData[dp] = 1;
                    } else {
                        this.academyBorrowData[dp] += 1;
                    }
                }
            });
            console.log(this.academyBorrowData);
            this.drawDepartment();
        },
        drawDepartment() {
            let sortedNumberArr = Object.entries(this.academyBorrowData).sort((a, b) => b[1] - a[1]);
            sortedNumberArr = sortedNumberArr.slice(0, 6).reverse();
            var chartDom = document.getElementById('department');
            var myChart = echarts.init(chartDom);
            var option;

            option = {
            title: {
                text: '入馆与借阅分布'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                type: 'shadow'
                }
            },
            legend: {},
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01]
            },
            yAxis: {
                type: 'category',
                data: sortedNumberArr.map(([key, _]) => key)
            },
            series: [
                {
                name: '入馆人数',
                type: 'bar',
                data: sortedNumberArr.map(([key, _]) => this.academyNumberData[key])
                },
                {
                name: '借阅数量',
                type: 'bar',
                data: sortedNumberArr.map(([_, value]) => value)
                }
            ]
            };

            option && myChart.setOption(option);
        }
    }
}
</script>

<style>
.bgpage{
    background: url(src/assets/true.png);
    height: 100vh;
    width: 100vw;
}
.container {
    display: flex; /* 将容器设置为 flex 容器 */
}
.box {
    flex: 1; /* 每个子元素占据相等的空间 */
    height: 300px;
    margin: 10px;
}
</style>
