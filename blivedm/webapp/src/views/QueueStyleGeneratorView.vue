<template>
  <div class="queue-style-generator container py-4">
    <NavBar />

    <!-- 预览区 -->
    <h3 class="mt-4">预览效果：</h3>
    <div id="preview" class="p-3 border rounded" :style="previewStyle">
      <div
        v-for="(user, index) in sampleQueue"
        :key="user.uname"
        class="queue-item mb-2"
        :class="{ 'fade-in': animation !== 'none' }"
        :style="queueItemStyle(user, index)"
      >
        <img :src="getAvatar(user.face)" />
        <span>
          {{ showIndex ? index + 1 + ". " + user.uname : user.uname }}
        </span>
      </div>
    </div>

    <!-- 控制区 -->
    <div class="row g-3 mt-4">
      <!-- 字体大小 -->
      <div class="col-md-4">
        <label class="form-label">字体大小(px)</label>
        <input type="number" class="form-control" v-model.number="fontSize" />
      </div>

      <!-- 字体颜色 -->
      <div class="col-md-4">
        <label class="form-label">文字颜色</label>
        <input type="color" class="form-control form-control-color" v-model="fontColor" />
      </div>

      <!-- 背景颜色 -->
      <div class="col-md-4">
        <label class="form-label">背景色</label>
        <input type="color" class="form-control form-control-color" v-model="bgColor" />
      </div>

      <!-- 背景透明度 -->
      <div class="col-md-4">
        <label class="form-label">背景透明度 (0–1)</label>
        <input
          type="number"
          step="0.01"
          min="0"
          max="1"
          class="form-control"
          v-model.number="bgOpacity"
        />
      </div>

      <!-- 阴影 -->
      <div class="col-md-4">
        <label class="form-label">是否启用阴影</label>
        <select class="form-select" v-model="shadow">
          <option value="none">无</option>
          <option value="light">轻微</option>
          <option value="strong">强烈</option>
        </select>
      </div>

      <!-- 圆角 -->
      <div class="col-md-4">
        <label class="form-label">圆角(px)</label>
        <input type="number" class="form-control" v-model.number="radius" />
      </div>

      <!-- 边框颜色 -->
      <div class="col-md-4">
        <label class="form-label">边框颜色</label>
        <input
          type="color"
          class="form-control form-control-color"
          v-model="borderColor"
        />
      </div>

      <!-- 边框宽度 -->
      <div class="col-md-4">
        <label class="form-label">边框宽度(px)</label>
        <input type="number" class="form-control" v-model.number="borderWidth" />
      </div>

      <!-- 行距 -->
      <div class="col-md-4">
        <label class="form-label">行距(px)</label>
        <input type="number" class="form-control" v-model.number="itemGap" />
      </div>

      <!-- 缩放 -->
      <div class="col-md-4">
        <label class="form-label">整体缩放(0.5–2)</label>
        <input
          type="number"
          step="0.1"
          min="0.5"
          max="2"
          class="form-control"
          v-model.number="scale"
        />
      </div>

      <!-- 模糊滤镜 -->
      <div class="col-md-4">
        <label class="form-label">模糊(0–20px)</label>
        <input
          type="number"
          min="0"
          max="20"
          class="form-control"
          v-model.number="blur"
        />
      </div>

      <!-- 显示序号 -->
      <div class="col-md-4">
        <label class="form-label">是否显示序号</label>
        <select class="form-select" v-model="showIndex">
          <option :value="true">是</option>
          <option :value="false">否</option>
        </select>
      </div>

      <!-- 动画 -->
      <div class="col-md-4">
        <label class="form-label">动画</label>
        <select class="form-select" v-model="animation">
          <option value="none">无</option>
          <option value="fade">淡入</option>
        </select>
      </div>

      <!-- 动画时长 -->
      <div class="col-md-4">
        <label class="form-label">动画时间(秒)</label>
        <input
          type="number"
          step="0.1"
          min="0.1"
          class="form-control"
          v-model.number="animationTime"
        />
      </div>
    </div>

    <!-- 按钮区 -->
    <div class="mt-4 d-flex gap-3">
      <button class="btn btn-primary" @click="applyStyles">生成 CSS</button>
      <button class="btn btn-success" @click="copyCSS">复制 CSS</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import NavBar from "@/components/NavBar.vue";

const defaultAvatar = new URL("@/assets/default_avatar.png", import.meta.url).href;

// 图片路径修复器
function getAvatar(path) {
  if (!path) return defaultAvatar;

  // 完整 URL 直接返回
  if (path.startsWith("http")) return path;

  // 只写文件名 → 自动转 assets 路径
  return new URL(`@/assets/${path}`, import.meta.url).href;
}

// ----- 控制变量 -----
const fontSize = ref(36);
const fontColor = ref("#ffffff");
const bgColor = ref("#000000");
const bgOpacity = ref(0.2);

const shadow = ref("none");
const radius = ref(8);
const borderColor = ref("#1E90FF");
const borderWidth = ref(5);
const itemGap = ref(5);

const scale = ref(1);
const blur = ref(0);

const showIndex = ref(true);

const animation = ref("fade");
const animationTime = ref(0.5);

const generatedCSS = ref("");

// 示例数据
const sampleQueue = ref([
  { uname: "muzimi", face: getAvatar("default_avatar.png"), color: "#ff6b6b" },
]);

// 预览整体样式
const previewStyle = computed(() => ({
  background: `${bgColor.value}${Math.floor(bgOpacity.value * 255)
    .toString(16)
    .padStart(2, "0")}`,
  filter: `blur(${blur.value}px)`,
  transform: `scale(${scale.value})`,
  transformOrigin: "top left",
}));

// 单项样式
function queueItemStyle(user) {
  return {
    fontSize: fontSize.value + "px",
    color: fontColor.value,
    backgroundColor: `${bgColor.value}${Math.floor(bgOpacity.value * 255)
      .toString(16)
      .padStart(2, "0")}`,
    borderLeft: `${borderWidth.value}px solid ${user.color}`,
    borderRadius: radius.value + "px",
    padding: "10px 20px",
    marginBottom: itemGap.value + "px",
    display: "flex",
    alignItems: "center",
    gap: "10px",
    boxShadow:
      shadow.value === "light"
        ? "0 0 10px rgba(0,0,0,0.2)"
        : shadow.value === "strong"
        ? "0 0 25px rgba(0,0,0,0.45)"
        : "none",
  };
}

// 构建 CSS
function applyStyles() {
  generatedCSS.value = `
.queue-item {
  font-size: ${fontSize.value}px;
  color: ${fontColor.value};
  background: ${bgColor.value}${Math.floor(bgOpacity.value * 255)
    .toString(16)
    .padStart(2, "0")};
  border-left: ${borderWidth.value}px solid ${borderColor.value};
  border-radius: ${radius.value}px;
  margin-bottom: ${itemGap.value}px;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  ${shadow.value === "light" ? "box-shadow: 0 0 10px rgba(0,0,0,0.2);" : ""}
  ${shadow.value === "strong" ? "box-shadow: 0 0 25px rgba(0,0,0,0.45);" : ""}
}

.queue-item img {
  object-fit: cover;
}

#preview {
  background: ${bgColor.value}${Math.floor(bgOpacity.value * 255)
    .toString(16)
    .padStart(2, "0")};
  filter: blur(${blur.value}px);
  transform: scale(${scale.value});
  transform-origin: top left;
}

${
  animation.value !== "none"
    ? `
.queue-item {
  animation: fadeIn ${animationTime.value}s ease;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
`
    : ""
}
`;
}

// 复制
function copyCSS() {
  navigator.clipboard.writeText(generatedCSS.value);
  alert("CSS 已复制！");
}
</script>

<style scoped>
.queue-item img {
  object-fit: cover;
}
img {
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
}
</style>
