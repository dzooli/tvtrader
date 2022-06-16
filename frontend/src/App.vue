<template>
  <v-app>
    <NavBar />
    <v-main>
      <v-toast />
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { VToast } from "vuetify-snackbar-toast";
export default {
  name: "App",
  data() {
    return {};
  },
  components: { NavBar, VToast },
  beforeMount() {
    this.$store.commit(
      "initialize",
      this.$ls.get("settings", this.$settings.$data),
      false
    );
  },
};
</script>
