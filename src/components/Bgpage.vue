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
                        title="测试子标题"
                        :boxb="true"
                    />
                </div>
                <div class="box">
                    <Viewbox
                        title="测试子标题"
                        :boxb="true"
                    />
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
    },
    methods: {
        loadHeatData() {
            // Load the JSON data asynchronously
            import('../../../data/03-检索热度.json')
                .then(module => {
                    // Once data is loaded, assign it to the heatData array
                    this.heatData = module.default.data;
                })
                .catch(error => {
                    console.error('Error loading heat data:', error);
                });
        },
        loadLibraryAttendanceData() {
            // Load the JSON data asynchronously
            let dateStr = `2023/${this.month}/${this.day}`;
            import('../../../data/05-2023年全年实时在馆人数-2分钟一更新.json')
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
