<template>
  <v-data-table
    :headers="headers"
    :items="alerts"
    class="elevation-1"
    :item-key="name"
  >
    <template v-slot:body="{ items, headers }">
      <tbody name="list" is="transition-group" v-if="items.length > 0">
        <tr
          v-for="item in items"
          :key="getRowId(item)"
          :class="getRowClass(item)"
          :id="getRowId(item)"
        >
          <td>{{ item.stratId }} - {{ item.stratName }}</td>
          <td>{{ item.symbol }}</td>
          <td>{{ item.direction }}</td>
          <td>{{ getTime(item.timestamp) }}</td>
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

<style>
.sell {
  background-color: crimson;
}
.buy {
  background-color: forestgreen;
}
.timeout {
  background-color: darkgrey;
}
.v-data-table-header {
  background-color: black;
}
.v-data-table {
  border: 1px solid wheat;
}
.theme--dark.v-data-table {
  color: yellow !important;
}
</style>

<script>
export default {
  name: "AlertTable",
  props: ["name"],
  data: () => ({
    headers: [
      { text: "Strategy" },
      { text: "Symbol" },
      { text: "Direction" },
      { text: "Time" },
    ],
    wsconnection: undefined,
  }),

  computed: {
    alerts: {
      get() {
        return this.$store.getters.alerts;
      },
    },
  },

  mounted: function () {
    this.$store.commit("startAlertTimer", this.updateAlertsTimeOut);
    this.wsconnection = new WebSocket(this.$store.getters.wsURL);
    if (this.wsconnection) {
      this.wsconnection.onmessage = (event) => {
        this.$store.commit("addAlert", JSON.parse(event.data));
      };
    } else {
      console.log("Cannot open the WebSocket to: " + this.$store.getters.wsURL);
    }
  },

  beforeDestroy: function () {
    this.$store.commit("stopAlertTimer");
    if (this.wsconnection) {
      this.wsconnection.close();
    }
  },

  methods: {
    getRowClass(alert) {
      let baseclass = "item-row ";
      return alert.timedout
        ? baseclass + "timedout"
        : alert.direction == "SELL"
        ? baseclass + "sell"
        : baseclass + "buy";
    },

    getRowId(item) {
      return item.stratId.toString() + item.symbol + item.timestamp;
    },

    getTime(timestamp) {
      let tsDate = new Date(timestamp * 1000);
      let timeArray = tsDate.toLocaleTimeString().split(" ");
      return timeArray[0];
    },

    updateAlertsTimeOut() {
      this.$store.commit("updateAlertsTimeOut");
    },
  },
};
</script>
