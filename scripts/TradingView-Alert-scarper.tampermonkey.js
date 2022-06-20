// ==UserScript==
// @name         TradingView - Alert scarper
// @version      0.1
// @description  Extracting TradingView alert text and sending it to http://localhost:8089 via JSON encoded POST. Alert panel must be open.
// @require      https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js
// @author       dzooli
// @match        https://www.tradingview.com/chart/*
// @connect      localhost
// @grant        GM_xmlhttpRequest
// ==/UserScript==

var $ = window.jQuery;

(function () {
  "use strict";
  const checkAlert = setInterval(() => {
    const alertTimeout = 15 * 60;
    const alertBody = $(
      "div.widgetbar-widget-alerts_log > div.widgetbar-widgetbody > div > :nth-child(2) > :nth-child(2) > div"
    ).first();
    let alertText = alertBody.contents().text().trim();
    if (alertText != "") {
      let alert = JSON.parse(alertText);
      let currTime = Date.now();
      let alrtTime = new Date(alert.timestamp);
      let alertTime = alrtTime.getTime();
      let bgColor = alertBody.css("background-color").toString();
      if (bgColor !== "rgb(128, 128, 128)" && bgColor !== "rgb(255, 0, 0)") {
        alertBody.css({
          background:
            (currTime - alertTime) / 1000 < alertTimeout ? "red" : "gray",
        });
        GM_xmlhttpRequest({
          url: "http://localhost:8089/",
          method: "POST",
          timeout: 10000,
          contentType: "application/json",
          data: JSON.stringify(alert),
          ontimeout: function (response) {
            console.error("TradingView Alert Scarper: Alert POST timeout!");
            alert(
              "Manual check required! Sending alert has been timed out: " +
                JSON.stringify(alert)
            );
          },
        });
      }
    }
  }, 5000);
})();
