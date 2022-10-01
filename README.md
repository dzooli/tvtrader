# TvTrader fullstack

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dzooli_tvtrader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dzooli_tvtrader)

## Description

This is a helper application for Tradingview alerts.

## Features

- Receive alerts from MultiBridge Chrome plugin
- Forward received alerts to the connected websocket clients
- Display latest alerts on the Web UI

## Stack

- Sanic for the Python backend
- Vue with Vuex and Vuetify for the frontend
- Docker for containerization (coming soon)

## Installation

### Backend

```bash
cd backend
python -m venv .
source Scripts/activate
pip install -f requirements.txt
```

### Frontend

```bash
cd frontend
npm -g i yarn
yarn install
```
