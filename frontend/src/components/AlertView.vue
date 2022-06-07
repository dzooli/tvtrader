<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>
    </v-row>

    <!-- Test input field -->
    <v-row justify="center">
      <v-col class="mb-4" cols="4" offset="1">
        <v-text-field
          label="Test Message in JSON format"
          :rules="rules"
          hide-details="auto"
          v-model="message"
        >
        </v-text-field>
      </v-col>
      <v-col class="mb-4" cols="2">
        <v-btn @click="addItem()" color="primary">Add Test</v-btn>
      </v-col>
    </v-row>

    <!-- Alert table -->
    <v-row justify="center">
      <v-col>
        <h1>Alerts</h1>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col><AlertTable /></v-col>
    </v-row>

    <v-row justify="center">
      <v-col class="mb-4" cols="6" offset="4"> </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AlertTable from "./AlertTable.vue";
export default {
  name: "AlertView",
  data: () => ({
    message: "",
    rules: [
      (value) => !!value || "Required",
      (value) =>
        (value && typeof value == "string" && value.length >= 5) ||
        "Minimum 5 characters",
    ],
  }),
  methods: {
    addItem() {
      var newAlert = JSON.parse(this.message);
      this.$store.commit("addAlert", newAlert);
    },
  },
  components: { AlertTable },
};
</script>
