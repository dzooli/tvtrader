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
    initialize(state, settings, justvaribales) {
      if (settings) {
        this.replaceState(Object.assign(state, settings));
      }
      if (!justvaribales) {
        state.alerts = [];
        state.alertTimer = undefined;
      }
    },

    addAlert(state, { stratId, stratName, symbol, direction, timestamp }) {
      let itemExists =
        state.alerts.find(function (current) {
          return current.timestamp == this;
        }, timestamp) || undefined;
      if (itemExists == undefined) {
        state.alerts.unshift({
          stratId: stratId,
          stratName: stratName,
          symbol: symbol,
          direction: direction,
          timestamp: timestamp,
          timedout:
            Date.now() / 1000 - timestamp > state.alertTimeout * 60
              ? true
              : false,
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
        el.timedout =
          Date.now() / 1000 - el.timestamp > state.alertTimeout * 60
            ? true
            : false;
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
