<template>
  <div class="container py-4">
    <NavBar />
    <h2 class="mb-4 text-center">关键词管理</h2>

    <div class="row g-4">
      <!-- 加入队列关键词 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">加入队列关键词</h5>
          </div>
          <div class="card-body">
            <div
              v-for="(word, index) in joinWords"
              :key="'join-' + index"
              class="d-flex mb-2"
            >
              <input
                v-model="joinWords[index]"
                class="form-control me-2"
                placeholder="输入关键词"
              />
              <button class="btn btn-danger btn-sm" @click="removeJoin(index)">
                删除
              </button>
            </div>
            <button class="btn btn-primary btn-sm mt-2" @click="addJoin">
              添加关键词
            </button>
          </div>
        </div>
      </div>

      <!-- 退出队列关键词 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">退出队列关键词</h5>
          </div>
          <div class="card-body">
            <div
              v-for="(word, index) in popWords"
              :key="'pop-' + index"
              class="d-flex mb-2"
            >
              <input
                v-model="popWords[index]"
                class="form-control me-2"
                placeholder="输入关键词"
              />
              <button class="btn btn-danger btn-sm" @click="removePop(index)">
                删除
              </button>
            </div>
            <button class="btn btn-primary btn-sm mt-2" @click="addPop">
              添加关键词
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 保存按钮 -->
    <div class="text-center mt-4">
      <button class="btn btn-success btn-lg" @click="saveKeywords">保存关键词</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

// --- 数据 ---
const joinWords = ref([]);
const popWords = ref([]);

// --- 加载服务器配置 ---
async function loadKeywords() {
  try {
    const res = await axios.get("http://localhost:5000/keywords");
    joinWords.value = res.data.join_words || [];
    popWords.value = res.data.pop_words || [];
  } catch (err) {
    console.error("加载关键词失败:", err);
  }
}

// --- 添加/删除 ---
function addJoin() {
  joinWords.value.push("");
}
function removeJoin(index) {
  joinWords.value.splice(index, 1);
}

function addPop() {
  popWords.value.push("");
}
function removePop(index) {
  popWords.value.splice(index, 1);
}

// --- 保存 ---
async function saveKeywords() {
  try {
    await axios.post("http://localhost:5000/keywords", {
      join_words: joinWords.value,
      pop_words: popWords.value,
    });
    alert("保存成功！");
  } catch (err) {
    console.error("保存关键词失败:", err);
    alert("保存失败");
  }
}

// --- 页面加载 ---
onMounted(() => {
  loadKeywords();
});
</script>

<style scoped>
input.form-control {
  flex: 1;
}
.card {
  min-height: 300px;
}
</style>
