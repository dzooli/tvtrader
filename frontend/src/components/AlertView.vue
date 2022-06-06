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

    <v-row justify="center">
      <v-col class="mb-4" cols="4" offset="1">
        <v-text-field
          label="Test Message"
          :rules="rules"
          hide-details="auto"
          v-model="message"
        ></v-text-field>
      </v-col>
      <v-col class="mb-4" cols="2">
        <v-btn @click="addItem()" color="primary">Add</v-btn>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col class="mb-4" cols="6" offset="4"> </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "AlertView",
  props: ["maxItems"],

  data: () => ({
    message: "",
    rules: [
      (value) => !!value || "Required",
      (value) =>
        (value && typeof value == "string" && value.length >= 5) ||
        "Minimum 5 characters",
    ],
    alerts: [],
  }),

  mounted() {
    this.alerts = new Array();
    this.alerts.push({ symbol: "EURUSD", direction: "BUY", timestamp: 12 });
  },

  methods: {
    addItem() {
      this.alerts.unshift({
        symbol: "GBPUSD",
        direction: "SELL",
        timestamp: 42,
      });
      if (this.alerts.length > this.maxItems) {
        this.alerts.splice(this.alerts.length - 1, 1);
      }

      console.log(this.alerts);
    },
  },
};
</script>
