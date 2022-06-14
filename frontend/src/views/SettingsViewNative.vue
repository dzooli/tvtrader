<template>
  <v-container>
    <v-row justify="center">
      <h1>Settings</h1>
    </v-row>
    <v-row justify="center">
      <v-col cols="6">
        <v-form lazy-validation v-model="Valid" ref="form">
          <v-container class="text-center">
            <v-text-field
              label="Alert Feed URL:"
              type="Text"
              :min="5"
              :counter="60"
              v-model="Field_URL"
              :rules="Rule_URL"
            ></v-text-field>
            <v-text-field
              label="Alert Timeout Refresh [s]:"
              type="Number"
              :min="1"
              :counter="2"
              v-model="Field_refresh"
              :rules="Rule_refresh"
            ></v-text-field>
            <v-text-field
              label="Alert Timeout [min]:"
              type="Number"
              :min="1"
              :counter="2"
              v-model="Field_timeout"
              :rules="Rule_timeout"
            ></v-text-field>
            <v-text-field
              label="Max Alert Count:"
              type="Number"
              :min="1"
              :counter="2"
              v-model="Field_maxcount"
              :rules="Rule_maxcount"
            ></v-text-field>
          </v-container>
        </v-form>
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
  data() {
    return {
      Valid: true,
      Field_URL: this.$store.getters.wsURL,
      Field_refresh: this.$store.getters.alertRefresh,
      Field_timeout: this.$store.getters.alertTimeout,
      Field_maxcount: this.$store.getters.maxAlerts,
      Rule_URL: [
        (v) => !!v || "Alert Feed URL is required",
        (v) => v.length <= 60 || "Max 60 characters",
      ],
      Rule_refresh: [
        (v) => !!v || "Alert Timeout Refresh is required",
        (v) => v.length <= 25 || "Max 25 characters",
      ],
      Rule_timeout: [
        (v) => !!v || "Alert Timeout is required",
        (v) => v.length <= 25 || "Max 25 characters",
      ],
      Rule_maxcount: [
        (v) => !!v || "Max Alert Count is required",
        (v) => v.length <= 25 || "Max 25 characters",
      ],
    };
  },
  methods: {
    saveSettings() {
      console.log("Saved");
    },
  },
};
</script>
