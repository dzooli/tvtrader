// ==UserScript==
// @name         TradingView - Alert scarper
// @version      0.2
// @description  Extracting TradingView alert text and sending it to http://localhost:8089/alert and /carbon-alert via JSON encoded POST. Alert panel must bwe open.
// @require      https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js
// @author       dzooli
// @match        https://www.tradingview.com/chart/*
// @connect      localhost
// @grant        GM_xmlhttpRequest
// ==/UserScript==

/* == Changes ==
 *
 * 06/23/2022:
 *   - Added the carbon-alert send feature
 *
*/

var $ = window.jQuery;

(function() {
    'use strict';
    const onceCheckInterval = 5000;
    const carbonCheckInterval = 30000;

    const sendSingleAlert= setInterval(() => {
        const alertTimeout = 15 * 60;
        const alertBody = $("div.widgetbar-widget-alerts_log > div.widgetbar-widgetbody > div > :nth-child(2) > :nth-child(2) > div").first();
        var bgColor = undefined;
        var alertText = alertBody.contents().text().trim();
        if (alertText != "") {
            var alert = JSON.parse(alertText);
            var currTime = Date.now();
            var alrtTime = new Date(alert.timestamp);
            var alertTime = alrtTime.getTime();
            bgColor = alertBody.css("background-color").toString();
        }
        // Send alert instantly but only once to the default POST endpoint
        if (bgColor !== undefined && bgColor !== "rgb(128, 128, 128)" && bgColor !== "rgb(255, 0, 0)" ) {
            alertBody.css({
                "background": (((currTime - alertTime) / 1000) < alertTimeout) ? "red" : "gray",
            });
            GM_xmlhttpRequest({
                url: "http://localhost:8089/alert",
                method: "POST",
                timeout: 10000,
                contentType: "application/json",
                data: JSON.stringify(alert),
                ontimeout: function(response) {
                    console.error("TradingView Alert Scarper: Alert POST timeout!");
                    alert("Manual check required! Sending alert has been timed out: " + JSON.stringify(alert));
                }
            });
        }
    }, onceCheckInterval);

    const sendRepeatedAlert= setInterval(() => {
        const alertTimeout = 15 * 60;
        const alertBody = $("div.widgetbar-widget-alerts_log > div.widgetbar-widgetbody > div > :nth-child(2) > :nth-child(2) > div").first();
        var bgColor = undefined;
        var alertText = alertBody.contents().text().trim();
        if (alertText != "") {
            var alert = JSON.parse(alertText);
            var currTime = Date.now();
            var alrtTime = new Date(alert.timestamp);
            var alertTime = alrtTime.getTime();
            bgColor = alertBody.css("background-color").toString();
            alertBody.css({
                "background": (((currTime - alertTime) / 1000) < alertTimeout) ? "red" : "gray",
            });
            // Send the last alert repeatedly to the Carbon-proxy POST endpoint
            GM_xmlhttpRequest({
                url: "http://localhost:8089/carbon-alert",
                method: "POST",
                timeout: 10000,
                contentType: "application/json",
                data: JSON.stringify(alert),
                ontimeout: function(response) {
                    console.error("TradingView Alert Scarper: Carbon Alert POST timeout!");
                    alert("Manual check required! Sending alert has been timed out: " + JSON.stringify(alert));
                }
            });
        }
    }, carbonCheckInterval);
})();
