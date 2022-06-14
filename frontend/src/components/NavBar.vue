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

    <v-btn text to="/">
      <span>Alerts</span>
    </v-btn>

    <v-spacer></v-spacer>

    <v-btn text to="/about">
      <span>About</span>
    </v-btn>

    <v-btn text to="/settings" title="Settings">
      <v-icon>mdi-cog-outline</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "NavBar",
};
</script>
