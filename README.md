# TvTrader fullstack

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dzooli_tvtrader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dzooli_tvtrader)

## Description

This is a full stack Sanic+Vue application for easily collect and process TradingView alerts. Includes a modular alert distribution layer in the ```agents``` directory.

Also a good candidate to learn more about test automation. **Pytest-BDD** is used for test automation, see the `tests` folder for examples.

**Do not use in production** as it is created for learning and personal use only. **No authentication** is implemented yet.

## Overview

![system overview](doc/tvtrader_schema.drawio.png)

## Features

- Receive alerts via custom scripts injected to TradingView using TamperMonkey
- Forward received alerts to the connected websocket clients
- Forward received alerts to a Graphite RRD for further processing (for example in Grafana)
- Display latest alerts on the Web UI
- Easy connection of external trading strategy alerts
- REST API (start the backend and go to [http://localhost:8089/swagger] for details)

### Distributor features

- Use Websocket as a source
- Use dynamically loaded distribution targets
  - Example target implementation is included with CLI
  - More is on way

### Example Grafana dashboard

![grafana dashboard](doc/grafana_dashboard.png)

## Stack

- Sanic for the backend
- Vue with Vuex and Vuetify for the frontend
- Docker for containerization (coming soon)

## Installation

Clone the repository and change the current directory to it.

```bash
git clone https://github.com/dzooli/tvtrader.git
cd tvtrader
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
    "stratName":"STARTNAME1",
    "symbol": "{{exchange}}:{{ticker}}",
    "interval":{{interval}},
    "direction":"{{strategy.order.comment}}",
    "timestamp": "{{timenow}}"
}
```

#### Example settings

![alert setting](doc/alert_setup.PNG)

### Enjoy

Start the backend first and the frontend. Open the frontend with your browser on [http://localhost:8080/] and wait for the alerts.

## Extras

In the `doc` folder you can find a Grafana dashboard example JSON file directly exported from my working setup.
