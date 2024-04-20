<template>
    <div class="bgpage">
        <Header></Header>
        <div>
            <div class="container">
                <div class="box">
                    <Viewbox
                        title=""
                        :boxb="true"
                    >
                        <div style="color: white; font-weight: bold; font-style: italic;">检索热度：</div><br>
                        <div id="myEchart" style="width: 100%; height: 40%;"></div><br>
                        <div style="color: white; font-weight: bold; font-style: italic;">新书榜单：</div><br>
                        <div id="newBook" style="color: white"> 1 段成式. 《神游大唐》. I242.1/A57-6 2023</div>
                        <div id="newBook" style="color: white"> 2 巴菲特. 《父亲巴菲特教我的事》. I712.55/E59 2023</div>
                        <div id="newBook" style="color: white"> 3 马瑟斯. 《Python编程》. TP311.56/I53 2023</div>
                    </Viewbox>
                </div>
                <div class="box">
                    <!-- 月份和日期输入框 -->
                    <div style="color: white">
                        月份：<input type="text" v-model="month" @input="updateDataStr">
                        日期：<input type="text" v-model="day" @input="updateDataStr"><br>
                    </div>
                    <Viewbox
                        title=""
                        :boxb="true"
                    >
                        <!-- 曲线图容器 -->
                        <div id="attendanceChart" style="width: 100%; height: 100%;"></div>
                    </Viewbox>
                </div>
                <div class="box">
                    <Viewbox
                        title="借还数据"
                        :boxb="true"
                    >
                        <Borrowgraph :fmonth="month" :fday="day"/>
                    </Viewbox>
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
            <div class="container">
                <div class="box">
                    <Viewbox
                        title="小组学习室/面试空间预约"
                        :boxb="true"
                    >
                        <Xzxxs/>
                    </Viewbox>
                </div>
                <div class="box">
                    <Viewbox
                        title="共享办公位热度"
                        :boxb="true"
                    >

                        <Officegraph/>
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
import 'echarts-wordcloud';
import Borrowgraph from './Borrowgraph.vue';
import Xzxxs from './Xzxxs.vue';
import Officegraph from './Officegraph.vue';
export default {
    components: {
        Header,
        Viewbox,
        Borrowgraph,
        Xzxxs,
        Officegraph
    },
    data() {
        return {
            subTitle: "子标题",
            heatData: [], // 保存检索热度数据
            entryData: [], // 保存入馆数据
            // 保存按 ID 分组的入馆数据
            groupedData: {本科: 1002523, 博士: 334600, 其他: 1158997, 研究生: 628196, 教师: 128236}, // 保存按 ID 分组的入馆数据
            // 保存各学院入馆人数
            academyNumberData: {'电子信息与电气工程学院': 469968, '船舶海洋与建筑工程学院': 103598, '安泰经济与管理学院': 163319, '密西根学院': 42696, '生命科学技术学院': 39516, '上海高级金融学院': 11166, '马克思主义学院': 46973, '机械与动力工程学院': 214586, '国际与公共事务学院': 43573, '凯原法学院': 162731, '药学院': 13647, '化学化工学院': 44273, '医学院': 101329, '材料科学与工程学院': 83326, '农业与生物学院': 49691, '生物医学工程学院': 34005, '外国语学院': 51002, '人力资源处（党委教师工作部）': 427, '图书馆': 32846, '航空航天学院': 30095, '巴黎卓越工程师学院': 22618, '数学科学学院': 64960, '媒体与传播学院': 44036, '海洋学院': 26466, '环境科学与工程学院': 22852, '设计学院': 44168, '物理与天文学院': 46360, '中英国际低碳学院': 6007, '招投标与政府采购办公室': 96, '教务处': 4808, '教育服务产业投资管理（集团）有限公司': 64, '后勤保障中心': 923, '人文学院': 37385, '变革性分子前沿科学中心': 1139, '教育学院': 12734, '中美物流研究院': 7119, '档案文博管理中心': 544, '巴黎高科卓越工程师学院': 1731, '上海交大-南加州大学文化创意产业学院': 10399, '党政办公室': 652, '党委宣传部': 175, '研究生院': 769, '教育技术中心': 236, '基建处': 187, '校友总会办公室': 266, '财务计划处': 1001, '分析测试中心': 538, '高等教育研究院': 1106, '李政道研究所': 7905, '智慧能源创新学院': 10140, '网络信息中心': 1306, '深远海全天候驻留浮式研究设施指挥部办公室': 6, '工会妇委会': 163, '系统生物医学研究院': 2309, '溥渊未来技术学院': 964, '科学技术发展研究院': 815, '转化医学研究院': 278, '资产管理与实验室处': 444, '学指委（学生处、团委、人武部）合署': 557, '个性化医学研究院': 360, '发展联络处': 57, '审计处': 107, '保卫处': 384, 'Bio-X研究院': 396, '国有资产监督管理委员会办公室': 37, '终身教育学院': 455, '教学发展中心': 273, '文科建设处': 105, '校园管理办公室': 68, '海洋装备研究院': 347, '学生创新中心': 711, '校区建设指挥部办公室': 28, '期刊中心': 357, '钱学森图书馆': 213, '规划发展处': 164, '致远学院': 470, '基础教育办公室': 11, '体育系': 2536, '国际合作与交流处': 398, '出版社有限公司': 33, '上海中医药大学': 1458, '李政道研究所建设指挥部办公室': 15, '自然科学研究院': 105, '党委组织部': 75, '党委统战部': 3, '人才交流中心': 43, '纪委办公室': 19, '党委巡察工作领导小组办公室': 109, '#N/A': 19, '元知机器人研究院': 6, '海洋水下工程科学研究院有限公司': 5, '信息安全管理办公室': 5, '张江高等研究院': 17, '专项建设办公室': 4, '日本研究中心': 9, '纪检监察机构': 1},
            // 保存各学院借阅数据
            academyBorrowData: {'医学院': 9801, '图书馆': 7582, '生物医学工程学院': 7029, '媒体与传播学院': 12013, '机械与动力工程学院': 34871, '物理与天文学院': 10468, '外国语学院': 11006, '船舶海洋与建筑工程学院': 20027, '药学院': 3084, '生命科学技术学院': 9270, '安泰经济与管理学院': 22405, '凯原法学院': 18219, '教育学院': 3259, '巴黎卓越工程师学院': 3166, '材料科学与工程学院': 16143, '人文学院': 17047, '教育技术中心': 463, '智慧能源创新学院': 2988, '上海高级金融学院': 2170, '国际与公共事务学院': 8082, '设计学院': 10405, '电子信息与电气工程学院': 61071, '致远学院': 484, '马克思主义学院': 12693, '分析测试中心': 759, '密西根学院': 5551, '农业与生物学院': 10034, '工会妇委会': 141, '后勤保障中心': 1080, '化学化工学院': 10185, '环境科学与工程学院': 5188, '网络信息中心': 726, '李政道研究所': 492, '航空航天学院': 6184, '个性化医学研究院': 191, '数学科学学院': 9182, '上海交大-南加州大学文化创意产业学院': 1360, '档案文博管理中心': 1087, '中英国际低碳学院': 1021, '财务计划处': 541, '学指委（学生处、团委、人武部）合署': 942, '终身教育学院': 1229, '基建处': 322, '教务处': 1358, '海洋学院': 2527, '系统生物医学研究院': 984, '人力资源处（党委教师工作部）': 573, '科学技术发展研究院': 547, '学生创新中心': 699, '国际合作与交流处': 305, '文科建设处': 129, '转化医学研究院': 308, '资产管理与实验室处': 328, '规划发展处': 227, '审计处': 190, '钱学森图书馆': 757, 'Bio-X研究院': 161, '巴黎高科卓越工程师学院': 306, '中美物流研究院': 834, '教学发展中心': 377, '体育系': 1171, '期刊中心': 108, '党委宣传部': 634, '党委组织部': 169, '张江高等研究院': 49, '党政办公室': 587, '海洋装备研究院': 264, '研究生院': 287, '纪委办公室': 67, '上海中医药大学': 774, '高等教育研究院': 110, '自然科学研究院': 162, '保卫处': 109, '发展联络处': 185, '溥渊未来技术学院': 91, '校园管理办公室': 10, '人才交流中心': 174, '党委统战部': 16, '变革性分子前沿科学中心': 51, '招投标与政府采购办公室': 194, '教育服务产业投资管理（集团）有限公司': 51, '出版社有限公司': 86, '校友总会办公室': 54, '国有资产监督管理委员会办公室': 16, '党委巡察工作领导小组办公室': 62, '专项建设办公室': 2, '深远海全天候驻留浮式研究设施指挥部办公室': 3},
            libraryAttendanceData: [], // 新建全年在馆人数数据
            month: '1', // 默认月份为1
            day: '31', // 默认日期为1
        }
    },
    mounted() {
        // Load the heat data when the component is mounted
        this.loadHeatData();
        this.initEchart();
        // Load the library attendance data when the component is mounted
        this.loadLibraryAttendanceData();
        this.drawPortrait();
        this.drawDepartment();
    },
    methods: {
        initEchart(){
    const initChart = () => {
        const echartDom = document.getElementById('myEchart')
        const myChart = echarts.init(echartDom)
        const option  = {
            series: [{
                type: 'wordCloud',
                shape: 'diamond',
                keepAspect: false,
                left: 'center',
                top: 'center',
                width: '100%',
                height: '100%',
                right: null,
                bottom: null,
                sizeRange: [12, 60], // 调整文字大小范围
                rotationRange: [0,0], // 调整文字旋转角度范围
                gridSize: 16, // 调整词云网格大小
                drawOutOfBound: false,
                layoutAnimation: true,
                textStyle: {
                    fontFamily: 'sans-serif',
                    fontWeight: 'bold',
                    color: function () {
                        // 使用明亮的颜色
                        return 'rgb(' + [
                            Math.round(50 + Math.random() * 205),
                            Math.round(50 + Math.random() * 205),
                            Math.round(50 + Math.random() * 205)
                        ].join(',') + ')';
                    }
                },
                emphasis: {
                    textStyle: {
                        textShadowBlur: 3,
                        textShadowColor: '#333'
                    }
                },
                data: this.heatData.map(function (item) {
                    console.log(item);
                    return {
                        name: item[0],
                        value: Math.sqrt(item[1])
                    }
                })
            }]
        };
        option && myChart.setOption(option)

        // 随着屏幕大小调节图表
        window.addEventListener("resize", () => {
            myChart.resize();
        });
    };

    if (document.readyState === 'complete') {
        initChart();
    } else {
        window.onload = initChart;
    }
        },
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
                console.log(this.heatData);
        },
        loadLibraryAttendanceData() {
            // Load the JSON data asynchro nously
            let dateStr = `2023/${this.month}/${this.day} `;
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
                    text: `${this.month}月${this.day}日实时在馆人数分布`,
                    left: 'center',
                        textStyle: {
                        color: '#FFFFFF' // 设置标题文字颜色为白色
                    }
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['主馆', '李政道图书馆', '包玉刚图书馆', '徐汇社科阅览室'],
                    textStyle: {
                        color: '#fff' // 设置图例文字颜色为白色
                    },
                    top: 30 // 设置图例的位置在图表上方，距离顶部 30px
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
                        },
                        textStyle: {
                            color: '#fff' // 设置坐标轴刻度文字颜色为白色
                        }
                    },
                    axisLine: {
                    lineStyle: {
                        color: '#fff' // 设置坐标轴线颜色为白色
                    }
                }
                }, 
                yAxis: {
                    type: 'value',
                    axisLine: {
                        lineStyle: {
                            color: '#fff' // 设置坐标轴线颜色为白色
                        }
                    },
                    axisLabel: {
                        textStyle: {
                            color: '#fff' // 设置坐标轴文字颜色为白色
                        }
                    }
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
            fetch('../../../data/02.json')
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
                        textStyle: {
                            color: '#FFFFFF' // Set the color of the legend to white
                        },
                        formatter: function (name) {
                            var target = myChart.getOption().series[0].data.find((item) => {return item.name === name});
                            return name + ' : ' + target.value;
                        }
                    },
                    series: [
                        {
                        name: '年总入馆人数',
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
                            fontWeight: 'bold',
                            color: '#FFFFFF'
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
            fetch('../../../data/01.json')
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
                text: '入馆与借阅分布',
                textStyle: {
                    color: '#FFFFFF'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                type: 'shadow'
                }
            },
            legend: {
                textStyle: {
                    color: '#FFFFFF'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                boundaryGap: [0, 0.01],
                axisLabel: {
                    color: '#FFFFFF'
                }
            },
            yAxis: {
                type: 'category',
                data: sortedNumberArr.map(([key, _]) => key),
                axisLabel: {
                    color: '#FFFFFF'
                }
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
