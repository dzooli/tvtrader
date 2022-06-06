import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    maxAlerts: 10,
    alerts: [],
  },
  getters: {
    alerts: (state) => state.alerts,
    maxAlerts: (state) => state.maxAlerts,
  },
  mutations: {
    addAlert(state, { symbol, direction, timestamp }) {
      state.alerts.unshift({
        symbol: symbol,
        direction: direction,
        timestamp: timestamp,
      });
      if (state.alerts.length > state.maxAlerts) {
        state.alerts.splice(state.alerts.length - 1, 1);
      }
    },
  },
  actions: {},
  modules: {},
});
