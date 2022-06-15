<template>
  <v-app>
    <NavBar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  name: "App",
  data() {
    return {};
  },
  components: { NavBar },
  beforeMount() {
    this.$store.commit(
      "initialize",
      this.$ls.get("settings", this.$settings.$data),
      false
    );
  },
};
</script>
