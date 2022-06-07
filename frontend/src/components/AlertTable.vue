<template>
  <v-data-table
    :headers="headers"
    :items="alerts"
    item-key="name"
    style="height: 700px"
  >
    <template v-slot:body="{ items, headers }">
      <tbody name="list" is="transition-group" v-if="items.length > 0">
        <tr v-for="item in items" :key="item.symbol" class="item-row">
          <td>{{ item.symbol }}</td>
          <td>{{ item.direction }}</td>
          <td>{{ item.timestamp }}</td>
          <td>{{ item.timedout }}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr>
          <td :colspan="headers.length" style="text-align: center">
            No Results Here!
          </td>
        </tr>
      </tbody>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: "AlertTable",
  data: () => ({
    headers: [
      { text: "Symbol" },
      { text: "Direction" },
      { text: "Timestamp" },
      { text: "Timed Out" },
    ],
  }),
  computed: {
    alerts: {
      get() {
        console.log("AlertTable get computed alerts called");
        console.log("Alert count: " + this.$store.getters.alerts.length);
        return this.$store.getters.alerts;
      },
    },
  },
  methods: {
    getSymbolColor(alert) {
      console.log("gegSymbolColor called with " + alert);
      if (alert.timedout) {
        return "lightgray";
      }
      if (alert.direction == "BUY") {
        return "green";
      }
      return "red";
    },
  },
};
</script>
