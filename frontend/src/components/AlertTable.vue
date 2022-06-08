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
    headers: [{ text: "Symbol" }, { text: "Direction" }, { text: "Time" }],
  }),

  computed: {
    alerts: {
      get() {
        return this.$store.getters.alerts;
      },
    },
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
  },
};
</script>
