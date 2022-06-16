// eslint-disable-next-line
<template>
  <v-app-bar app color="primary">
    <div class="d-flex align-center">
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
        transition="scale-transition"
        width="42"
      />

      <v-img
        alt="Vuetify Name"
        class="shrink mt-1 hidden-sm-and-down"
        contain
        min-width="100"
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
        width="100"
      />
    </div>

    <v-spacer class="col-1"></v-spacer>

    <v-btn text to="/" title="Alerts">
      <v-icon>mdi-bell-alert-outline</v-icon>
    </v-btn>

    <v-spacer></v-spacer>

    <v-btn text to="/about" title="About">
      <v-icon>mdi-information-outline</v-icon>
    </v-btn>

    <v-btn text to="/settings" title="Settings">
      <v-icon>mdi-cog-outline</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "NavBar",
  computed: {
    toastVisible: {
      get() {
        return this.$store.getters.toastMessage != "";
      },
      set() {
        return true;
      },
    },
    toastMessage: {
      get() {
        return this.$store.getters.toastMessage;
      },
    },
  },
};
</script>
