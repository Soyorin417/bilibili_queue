<template>
  <div>
    <NavBar> </NavBar>
    <div class="container mt-3" style="max-width: 500px">
      <h3>编辑直播间配置</h3>

      <div class="mt-3">
        <label>直播间 ID（可多个）</label>
        <input
          v-model="roomIds"
          class="form-control"
          placeholder="例如：31727215, 123456"
        />
      </div>

      <div class="mt-3">
        <label>SESSDATA</label>
        <input v-model="sessdata" class="form-control" />
      </div>

      <button class="btn btn-primary mt-3" @click="saveConfig">保存配置</button>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "HomeView",
  components: {
    NavBar,
  },
  data() {
    return {
      roomIds: "",
      sessdata: "",
    };
  },

  async created() {
    const res = await fetch("/api/config");

    const json = await res.json();
    this.roomIds = json.TEST_ROOM_IDS.join(", ");
    this.sessdata = json.SESSDATA;
  },

  methods: {
    async saveConfig() {
      await fetch("/api/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          TEST_ROOM_IDS: this.roomIds.split(",").map((v) => Number(v.trim())),
          SESSDATA: this.sessdata,
        }),
      });

      alert("保存成功！");
    },
  },
};
</script>
<style scoped></style>
