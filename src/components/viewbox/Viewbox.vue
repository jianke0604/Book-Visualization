<template>
    <div
        class="data-box"
        :class="{ noborder: !boxb }"
        :style="{ height: '100%', width: '100%'}"
    >
        <!--左上边框-->
        <div class="line-box" v-if="boxb">
            <i class="t-l-line"></i>
            <i class="l-t-line"></i>
        </div>
        <!--右上边框-->
        <div class="line-box" v-if="boxb">
            <i class="t-r-line"></i>
            <i class="r-t-line"></i>
        </div>
        <!--左下边框-->
        <div class="line-box" v-if="boxb">
            <i class="l-b-line"></i>
            <i class="b-l-line"></i>
        </div>
        <!--右下边框-->
        <div class="line-box" v-if="boxb">
            <i class="r-b-line"></i>
            <i class="b-r-line"></i>
        </div>
        <div class="in-title" v-if="title.length > 0">{{ title }}</div>
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: "databox",
    props: {
        title: String,
        boxb: {//是否显示边框
            type: Boolean,
            default: true
        }
    }
};
</script>
  
<style>
@import "./index";
.word-cloud {
    position: relative;
    width: 100%;
    height: 100%;
}

.word-cloud div {
    position: absolute;
    display: inline-block;
    border: 1px solid #290665; /* 圆形边框 */
    border-radius: 50%; /* 圆形边框 */
    padding: 5px; /* 调整圆形内边距 */
    background-color: #239ec7; /* 圆形背景色 */
    white-space: nowrap; /* 防止关键词换行 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}
</style>
