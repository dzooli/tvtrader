import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    devmode: true,
    alertTimeout: 1, // timeout for the alert in minutes
    alertUpdateTime: 5, // timeout update interval in seconds
    alertTimer: undefined,
    maxAlerts: 10,
    alerts: [],
  },

  getters: {
    alerts: (state) => state.alerts,
    maxAlerts: (state) => state.maxAlerts,
    devmode: (state) => state.devmode,
    alertTimeout: (state) => state.alertTimeout,
  },

  mutations: {
    /**
     * Add the received alert and calculate if it is already timed out.
     * Timeout value is defined in the state and given in minutes.
     *
     * @param {*} state
     * @param {*} param1
     */
    addAlert(state, { stratId, symbol, direction, timestamp }) {
      state.alerts.unshift({
        stratId: stratId,
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
  },

  actions: {},

  modules: {},
});
