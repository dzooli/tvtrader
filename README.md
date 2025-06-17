# TvTrader fullstack

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-orange.svg)](https://sonarcloud.io/summary/new_code?id=dzooli_tvtrader)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dzooli_tvtrader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dzooli_tvtrader) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dzooli_tvtrader&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dzooli_tvtrader)

## Description

This is a full stack Sanic+Vue application for easily collect and process TradingView alerts and possibly execute custom trading strategies. Includes a modular alert distribution layer in the ```agents``` directory.

Also a good candidate to learn more about test automation. **Pytest-BDD** is used for test automation, see the `tests` folder for examples.

**Do not use in production** as it is created for learning and personal use only. **No authentication** is implemented yet.

## Overview

[_C4_diagram_here_]

```plantuml
@startuml C4_Elements
!include  <C4/C4_Container>

LAYOUT_WITH_LEGEND()

AddElementTag("dev", $fontColor="yellow")
AddRelTag("future", $textColor="lightgrey", $lineColor="grey", $lineStyle = DashedLine())
Person(user, "Users")

System_Ext(tradingview, "TradingView", "Data source")
Container(tvtrader_frontend, "Frontend", "VueJs", "Alert dashboard")

System_Boundary(data_backend, "Data Backend") {
  Container(fetcher, "Fetcher", "REST, NestJs", "Allows users to dinamycally fetch price data from TradingView")
  SystemDb(influx, "Store", "InfluxDB, FluxScript")
  Container(tvtrader_backend, "Backend", "WS, REST", "API backend for the dashboard")
  Container(tvtrader_distributor, "Distributor", "Python", "Receiver and distributor for the alerts")
}
SystemQueue(alertq, "Alert Queue")

System_Boundary(dist_targets, "Distribution Targets") {
  Person(sysdev, "Target developer", $tags="dev")
  Container(carbon, "CarbonDB", "Optional target for the alerts")
  Container(grafana, "Grafana", "Optional target for the alerts")
  Container(logging, "Logging", "Optional loogging for the alerts")
  Container(opt_target, "...", "Other types of distribution targets")
  Container_Ext(future_frontend, "Future Frontend", "Vue3+Quasar")
  Rel_D(sysdev, opt_target, "Implements distribution target")
  Rel_U(sysdev, carbon, "Implements distribution target")
  Rel_L(sysdev, grafana, "Implements distribution target")
  Rel_R(sysdev, logging, "Implements distribution target")
  Rel_U(sysdev, future_frontend, "Implements features", $tags="future")
}

System_Boundary(strategies, "Strategy evaluators") {
  Container(strategy_1, "Jupyter", "NumPy, Pandas", "Evaluator for the strategy")
  Container(opt_strategy, "Others", "Various technologies", "Additional evaluators")
  Person(quant, "Quantitative Developer", $tags="dev")
  System_Boundary(browser, "Browser") {
    Container_Ext(tvui, "TradingView UI", "User interface for TradingView")
    Container(alertmonitor, "Monitoring script", "Monitor for the alert panel")
    Container(monkey, "TamperMonkey plugin", "Executor")
    Rel_D(monkey, alertmonitor, "Injects and executes the script")
    Rel(tvui, alertmonitor, "Provides alerts")
    Rel(tradingview, tvui, "Sends prices, executes PineScript strategies")
  }

}

Rel(tvtrader_distributor, alertq, "Distributes the alerts", "ThreadPool")
Rel(alertq, dist_targets, "Receives and processes the alerts")

Rel(tradingview, fetcher, "Fetches prices", "HTTPS GET")
Rel(fetcher, influx, "Gets specific prices periodaically", "REST GET")
Rel_R(influx, strategies, "Reads the prices and calculates the strategy action", "API")
Rel_U(strategies, tvtrader_backend, "Sends strategy alerts", "REST POST")
Rel_R(tvtrader_backend, tvtrader_frontend, "Receives alerts for visualization", "WebSocket")
Rel(tvtrader_backend, tvtrader_distributor, "Receives alerts for distribution", "WebSocket")
Rel_U(user, tvtrader_frontend, "Monitors the alerts")
Rel_U(user, future_frontend, "Monitors the alerts", $tags="future")
Rel_U(quant, opt_strategy, "Implements strategies")
Rel_U(quant, strategy_1, "Implements strategies")
@enduml
```


## Features

### Fetcher

- Receiving price information from TradingView
- Publishing the prices upon HTTP GET in JSON format

### Store

- InfluxDB FluxScript to store the price information from the fetcher - (WIP)

### Backend

- Receiving alerts via HTTP PUST (for example by custom scripts injected to TradingView using TamperMonkey)
- Forwarding received alerts to the connected websocket clients
- REST API (start the backend and go to [http://localhost:8089/swagger] for details)

### Distributor

- Receive alerts from various sources (currently the backend's websocket)
- Forwarding alerts to the connected distribution targets
- Loading of distribution targets upon startup from a directory
  - Example console target implementation is included with a CLI

### Frontend

- Receiving incoming alerts from the connected backend
- Displaying latest alerts on the Web UI
- Configurable timeout for the alerts
- Color coding the status of the alerts

## Tech stack

- Python
  - Sanic framework for the backend
- Javascript
  - Vue with Vuex and Vuetify for the frontend
  - Nest.js for the fetcher
  - For the TamperMonkey scripts
- Docker for containerization (coming soon)

## Installation

Clone the repository and change the current directory to it.

```bash
git clone https://github.com/dzooli/tvtrader.git
cd tvtrader
```

### Testing

Use the requirements_dev.txt for virtualenv creation:

```bash
python -m venv .
source venv/bin/activate
pip install -r backend/requirements.txt
pip install -r backend/requirements_dev.txt
pytest backend
pytest agents/tvt_agents
```

### Backend

Using a **Linux** environment:

```bash
python -m venv .
source bin/activate
pip install -r requirements.txt
```

#### Start backend

```bash
cd backend
./start.sh
```

```bash
# or after manual venv activation
python -m src.server
```

Under Windows the virtualenv creates a different directory structure and activation will also be different. Please read the virtualenv related documentation first.

### Frontend

```bash
cd frontend
npm -g i yarn
yarn install
```

#### Start frontend

```bash
cd frontend
yarn serve # For development. Use 'yarn build' for production use and deploy it in your preferred way.
```

## Usage

### Alert catching setup

Install TamperMonkey Chrome extension and add the scripts from the `scripts` directory. Restrict them to run only on `https://tradingview.com/charts/*` on the settings page and **do other security related settings as you wish.** Do not forget, TamperMonkey is a powerful but double-edged tool.

Open TradingView, login and display the alerts panel. Add a properly formatted alert following the directions below.

### TradingView alert setup

#### General rules

- Do not add blocking pop-up window
- Do not add disturbing actions
- Use the strategy.comment as "BUY" or "SELL" only
- Keep the Alerts panel open (the page script is based on this panel)

#### Alert message content

```json
{
    "stratId":1,
    "stratName": "STRATEGY_NAME1",
    "symbol": "{{exchange}}:{{ticker}}",
    "interval": {{interval}},
    "direction": "{{strategy.order.comment}}",
    "timestamp": "{{timenow}}"
}
```

#### Example settings

![alert setting](doc/alert_setup.PNG)

### Enjoy

Start the backend first and the frontend. Open the frontend with your browser on [http://localhost:8080/] and wait for the alerts.

## Extras

In the `doc` folder you can find various useful information as well as the developer documentation (WIP).
