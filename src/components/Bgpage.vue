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
                    <Viewbox
                        :title="subTitle"
                        :boxb="true"
                    />
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
export default {
    components: {
        Header,
        Viewbox
    },
    data() {
        return {
            subTitle: "子标题",
            heatData: []
        }
    },
    mounted() {
        // Load the heat data when the component is mounted
        this.loadHeatData();
    },
    methods: {
        loadHeatData() {
            // Load the JSON data asynchronously
            import('../../../data/03-检索热度.json')
                .then(module => {
                    // Once data is loaded, assign it to the heatData array
                    this.heatData = module.default.data;
                    // console.log('成功加载热度数据:', this.heatData);
                    // console.log('成功加载热度数据:', this.heatData[0][0], this.heatData[0][1]);
                })
                .catch(error => {
                    console.error('Error loading heat data:', error);
                });
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