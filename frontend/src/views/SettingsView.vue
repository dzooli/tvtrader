<template>
  <v-container>
    <v-row justify="center">
      <h1>Settings</h1>
    </v-row>
    <v-row>
      <v-col cols="6" offset="3">
        <v-form-generator
          :model="model"
          :schema="schema"
          :options="options"
          ref="form"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="2" offset="7">
        <v-btn @click="saveSettings()">Save</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  components: {
    "v-form-generator": require("vuetify-form-generator").default,
  },
  data() {
    return {
      model: {
        url: this.$store.getters.wsURL,
        timeout: this.$store.getters.alertTimeout,
        refresh: this.$store.getters.alertRefresh,
        maxnum: this.$store.getters.maxAlerts,
      },
      schema: {
        fields: [
          {
            type: "text",
            name: "url",
            model: "url",
            label: "Alert Feed URL:",
            required: true,
          },
          {
            type: "text",
            name: "alert-timeout",
            model: "timeout",
            label: "Alert Timeout [min]:",
            required: 1,
          },
          {
            type: "text",
            name: "timeout-refresh",
            model: "refresh",
            label: "Alert Status Refresh [s]:",
            required: true,
          },
          {
            type: "text",
            name: "max-alert-num",
            model: "maxnum",
            label: "Maximum Alert Count:",
          },
        ],
      },
      options: {},
    };
  },
  methods: {
    saveSettings() {
      console.log("Saved");
      console.log(this.$refs.form.$children[0].localValue);
    },
  },
};
</script>
