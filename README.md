# TvTrader fullstack

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
pip install -f requirements.txt
source Scripts/activate
```

### Frontend

```bash
cd frontend
npm -g i yarn
yarn install
```
