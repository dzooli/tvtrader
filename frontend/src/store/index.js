// eslint-ignore-next-line
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        devmode: "",
        alertTimeout: "", // timeout for the alert in minutes
        alertUpdateTime: "", // timeout update interval in seconds
        alertTimer: undefined,
        maxAlerts: "",
        wsURL: "",
        alerts: [],
    },

    getters: {
        alerts: (state) => state.alerts,
        maxAlerts: (state) => state.maxAlerts,
        devmode: (state) => state.devmode,
        alertTimeout: (state) => state.alertTimeout,
        alertRefresh: (state) => state.alertUpdateTime,
        wsURL: (state) => state.wsURL,
    },

    mutations: {
        initialize(state, settings, removealerts) {
            if (settings) {
                this.replaceState(Object.assign(state, settings));
            }
            if (removealerts) {
                state.alerts = [];
                state.alertTimer = undefined;
            }
        },

        addAlert(state, { id, name, symbol, direction, timestamp }) {
            // Close first
            if (direction.toUpperCase().startsWith("CLOSE")) {
                let closing = false;
                for (let el of state.alerts) {
                    if (
                        el.stratName == name &&
                        el.stratId == id &&
                        el.symbol == symbol
                    ) {
                        el.status = "closed";
                        closing = true;
                    }
                }
                if (closing) {
                    return;
                }
            }

            // Find existing alert on same strat and pair
            let itemExists = state.alerts.findIndex(
                function (current) {
                    return (
                        current.timestamp == this.timestamp &&
                        current.stratId == this.id &&
                        current.stratName == this.name &&
                        current.symbol == this.symbol
                    );
                },
                { timestamp: timestamp, id: id, name: name, symbol: symbol }
            );
            // No existing alert => add to list
            if (itemExists == -1) {
                state.alerts.unshift({
                    stratId: id,
                    stratName: name,
                    symbol: symbol,
                    direction: direction,
                    timestamp: timestamp,
                    status:
                        Date.now() / 1000 - timestamp > state.alertTimeout * 60
                            ? "active"
                            : "invalidated",
                });
            }
            // Cut the list to max items
            if (state.alerts.length > state.maxAlerts) {
                state.alerts.splice(state.alerts.length - 1, 1);
            }
        },

        setDevMode(state, mode) {
            state.devmode = mode;
        },

        setAlertTimeout(state, timeOut) {
            state.alertTimeout = timeOut;
        },

        startAlertTimer(state, func) {
            state.alertTimer = setInterval(func, state.alertUpdateTime * 1000);
        },

        stopAlertTimer(state) {
            clearInterval(state.alertTimer);
        },

        updateAlertsTimeOut(state) {
            for (let el of state.alerts) {
                el.status =
                    Date.now() / 1000 - el.timestamp >
                        state.alertTimeout * 60 && el.status != "closed"
                        ? "invalidated" // invalidate the alert on timeout
                        : el.status; // Status not changed
            }
        },

        setWsURL(state, url) {
            if (typeof url == "string") {
                state.wsURL = url;
            }
        },

        setMaxAlerts(state, maxAlertCount) {
            state.maxAlerts = maxAlertCount;
        },

        setAlertRefresh(state, refresh) {
            state.alertUpdateTime = refresh;
            if (state.alertTimer != undefined) {
                this.commit("stopAlertTimer");
                this.commit("startAlertTimer");
            }
        },
    },

    actions: {},

    modules: {},
});
