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
    message: "",
  },

  getters: {
    alerts: (state) => state.alerts,
    maxAlerts: (state) => state.maxAlerts,
    devmode: (state) => state.devmode,
    alertTimeout: (state) => state.alertTimeout,
    alertRefresh: (state) => state.alertUpdateTime,
    wsURL: (state) => state.wsURL,
    toastMessage: (state) => state.message,
  },

  mutations: {
    initialize(state, settings, justvaribales) {
      if (settings) {
        this.replaceState(Object.assign(state, settings));
      }
      if (justvaribales == false) {
        state.alerts = [];
        state.alertTimer = undefined;
        state.message = "";
      }
    },

    setToast(state, message) {
      state.message = message;
    },

    clearToast(state) {
      state.message = "";
    },

    addAlert(state, { stratId, stratName, symbol, direction, timestamp }) {
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
      console.log("alert timer started");
    },

    stopAlertTimer(state) {
      clearInterval(state.alertTimer);
      console.log("alert timer stopped");
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
