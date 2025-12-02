<template>
  <div>
    <NavBar></NavBar>
    <QueueDisplay></QueueDisplay>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import QueueDisplay from "@/components/QueueDisplay.vue";
export default {
  name: "QueueDisplayView",
  components: {
    QueueDisplay,
    NavBar,
  },
};
</script>

<style scoped></style>
