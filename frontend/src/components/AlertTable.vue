<template>
    <v-data-table
        :headers="headers"
        :items="alerts"
        :class="tableConnected"
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
.closed {
    background-color: orange;
}
.invalidated {
    background-color: darkgrey;
}
.v-data-table-header {
    background-color: black;
}
.disconnected {
    border: 1px solid red !important;
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
    event: ["wserror"],
    data: () => ({
        headers: [
            { text: "Strategy" },
            { text: "Symbol" },
            { text: "Direction" },
            { text: "Time" },
        ],
        wsconnection: undefined,
        tableConnected: "elevation-1 disconnected",
    }),

    computed: {
        alerts: {
            get() {
                return this.$store.getters.alerts;
            },
        },
    },

    mounted: function () {
        this.$toast.warn("Connecting to the backend...");
        this.$store.commit("startAlertTimer", this.updateAlertsTimeOut);
        this.wsconnection = new WebSocket(this.$store.getters.wsURL);
        this.wsconnection.onmessage = (event) => {
            this.$store.commit("addAlert", JSON.parse(event.data));
        };
        this.wsconnection.onclose = () => {
            if (this.$route.name === "alerts") {
                this.$toast.danger(
                    "Backend disconnected! Fix the issue and reload the page!",
                    { timeout: -1 }
                );
                this.tableConnected = "elevation-1 disconnected";
            }
        };
        setTimeout(() => {
            if (this.wsconnection.readyState !== WebSocket.OPEN) {
                this.$toast.danger(
                    "Failed to connect to the backend service! Fix the issue and reload the page!"
                );
                this.tableConnected = "elevation-1 disconnected";
            } else {
                this.tableConnected = "elevation-1";
            }
        }, 5000);
    },

    beforeDestroy: function () {
        this.$store.commit("stopAlertTimer");
        if (this.wsconnection.readyState == WebSocket.OPEN) {
            this.wsconnection.close();
        }
    },

    methods: {
        getRowClass(alert) {
            return (
                "item-row " +
                alert.status +
                " " +
                (alert.direction == "SELL" ? "sell" : "buy")
            );
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
