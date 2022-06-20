// ==UserScript==
// @name         TradingView - Alert scarper
// @version      0.1
// @description  Extracting TradingView alert text and sending it to http://localhost:8089 via JSON encoded POST. Alert panel must bwe open.
// @require      https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js
// @author       dzooli
// @run-at       document-idle
// @match        https://www.tradingview.com/chart/*
// @connect      localhost
// @grant        GM_xmlhttpRequest
// ==/UserScript==

var $ = window.jQuery;

(function() {
    'use strict';
    const checkAlert= setInterval(() => {
        /** For development purposes, send test data **/
        let testData = {
            "stratId": 2,
            "symbol": "FXCM:GBPUSD",
            "stratName": "TEST",
            "direction": "BUY",
            "interval": 15,
            "timestamp": "2019-08-27T09:56:00Z"
        };
        GM_xmlhttpRequest({
            url: "http://localhost:8089/",
            method: "POST",
            timeout: 5,
            contentType: "application/json",
            data: JSON.stringify(testData),
        });
        /** Dev test section end **/

        const alertTimeout = 15 * 60;
        const alertBody = $("div.widgetbar-widget-alerts_log > div.widgetbar-widgetbody > div > :nth-child(2) > :nth-child(2) > div").first();
        let alertText = alertBody.contents().text().trim();
        if (alertText != "") {
            let alert = JSON.parse(alertText);
            let currTime = Date.now();
            let alrtTime = new Date(alert.timestamp);
            let alertTime = alrtTime.getTime();
            alertBody.css({
                "background": (((currTime - alertTime) / 1000) < alertTimeout) ? "red" : "gray",
            });
            GM_xmlhttpRequest({
                url: "http://localhost:8089/",
                method: "POST",
                timeout: 5,
                contentType: "application/json",
                data: JSON.stringify(alert),
            });
        }
    }, 5000);
})();
