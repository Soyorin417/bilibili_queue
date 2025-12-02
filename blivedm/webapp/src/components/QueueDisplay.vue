<template>
  <div class="queue-display">
    <div class="row mb-3">
      <div class="col-2">
        <!-- 搜索 -->
        <div class="search-user">
          <input v-model="searchQuery" placeholder="搜索用户名" />
        </div>
      </div>
      <div class="col-4"></div>
      <div class="col-6">
        <!-- 入队区域 -->
        <div class="add-user">
          <input v-model="newUserName" placeholder="用户名" />
          <input v-model="newUserFace" placeholder="头像 URL" />
          <button class="btn" @click="addToQueue">入队</button>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">
      {{ error }}
      <button class="btn" @click="fetchQueue">重试</button>
    </div>

    <!-- 队列展示 -->
    <div id="preview" class="mt-3">
      <div v-if="filteredQueue.length === 0" class="empty">（无人）</div>
      <transition-group name="fade" tag="div">
        <div
          v-for="(user, index) in filteredQueue"
          :key="user.uid"
          class="queue-item mt-3"
          :id="'user-' + user.uid"
          :style="{ borderLeftColor: user.color || '#1E90FF' }"
        >
          <img :src="user.face || 'default_avatar.png'" :alt="user.uname" />
          <span>{{ index + 1 }}. {{ user.uname }}</span>
          <div class="actions">
            <button class="btn-small" @click="removeFromQueue(user.uid)">出队</button>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "QueueDisplay",
  data() {
    return {
      queue: [],
      error: "",
      newUserName: "",
      newUserFace: "",
      searchQuery: "", // 搜索关键词
    };
  },
  computed: {
    filteredQueue() {
      if (!this.searchQuery.trim()) return this.queue;
      const q = this.searchQuery.trim().toLowerCase();
      return this.queue.filter((user) => user.uname.toLowerCase().includes(q));
    },
  },
  mounted() {
    this.fetchQueue();
    this.interval = setInterval(this.fetchQueue, 1000);
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    async fetchQueue() {
      try {
        const res = await fetch("/api/queue?_=" + Date.now());
        if (!res.ok) throw new Error(res.statusText);
        const arr = await res.json();
        this.queue = arr || [];
        this.error = "";
      } catch (e) {
        console.error("读取 queue.json 失败:", e);
        this.error = "读取 queue.json 失败: " + e.message;
        this.queue = [];
      }
    },

    async saveQueue(newQueue) {
      try {
        const res = await fetch("/api/queue", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(newQueue),
        });
        if (!res.ok) throw new Error(res.statusText);
        this.queue = newQueue;
      } catch (e) {
        console.error("更新 queue.json 失败:", e);
        this.error = "更新队列失败: " + e.message;
      }
    },

    removeFromQueue(uid) {
      const newQueue = this.queue.filter((u) => u.uid !== uid);
      this.saveQueue(newQueue);
    },

    addToQueue() {
      if (!this.newUserName.trim()) return;
      const newUid = Date.now(); // 简单生成唯一 UID
      const newEntry = {
        uid: newUid,
        uname: this.newUserName.trim(),
        face: this.newUserFace || "default_avatar.png",
        color: "#" + Math.floor(Math.random() * 16777215).toString(16),
      };
      const newQueue = [...this.queue, newEntry];
      this.saveQueue(newQueue);
      this.newUserName = "";
      this.newUserFace = "";
    },
  },
};
</script>

<style scoped>
.queue-display {
  font-family: "Microsoft YaHei", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #fff;
  padding: 20px;

  /* 关键：给内容右移，避开 sidebar */
  margin-left: 220px; /* 200px sidebar + 20px间距 */
}

#preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 15px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 15px rgba(156, 16, 16, 0.651);
}

.queue-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 20px;
  border-left: 6px solid #1e90ff;
  border-radius: 10px;
  background: rgba(14, 165, 170, 0.596);
  font-size: 28px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.queue-item img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.actions {
  margin-left: auto;
}

.btn-small {
  padding: 4px 10px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  background: #ff6b6b;
  color: #fff;
  cursor: pointer;
  margin-left: 10px;
}

.btn-small:hover {
  background: #ff4b4b;
}

.add-user {
  display: flex;
  gap: 10px;
}

.add-user input {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #888;
  flex: 1;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background: #1e90ff;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}
.btn:hover {
  background: #1c86ee;
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.empty {
  font-size: 32px;
  color: #aaa;
  text-align: center;
  padding: 30px 0;
}

.error {
  margin-bottom: 15px;
  color: #f88;
}

.search-user input {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #888;
  width: 100%;
}
</style>
