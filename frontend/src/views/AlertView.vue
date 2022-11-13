<template>
  <v-container>
    <!-- Test input field -->
    <v-row v-if="this.$store.getters.devmode" justify="center">
      <v-col class="mb-4" cols="4" offset="1">
        <v-text-field
          label="Test Message in JSON format"
          :rules="rules"
          hide-details="auto"
          v-model="message"
        >
        </v-text-field>
      </v-col>
      <v-col class="mb-4 pa-10" cols="2">
        <v-btn @click="addItem()" color="success">Add Test</v-btn>
      </v-col>
    </v-row>

    <!-- Alert table -->
    <v-row justify="center">
      <v-col cols="11"><AlertTable name="main-alerts" /></v-col>
    </v-row>

    <v-row justify="center">
      <v-col class="mb-4" cols="6" offset="4"> </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AlertTable from "@/components/AlertTable.vue";
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
      let newAlert;
      try {
        newAlert = JSON.parse(this.message);
      } catch (error) {
        this.$toast.danger(error.toString());
        return;
      }

      this.$axios.post("/alert", newAlert).catch((error) => {
        this.$toast.danger(error.toString());
      });
    },
  },
  components: { AlertTable },
};
</script>
