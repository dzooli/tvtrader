AlertSchema = {
    "type": "object",
    "required": ["stratId", "stratName", "symbol", "direction", "timestamp", "interval"],
    "properties": {
        "stratId":      {"type": "number", "minimum": 0},
        "stratName":    {"type": "string"},
        "symbol":       {"type": "string"},
        "interval":     {"type": "number"},
        "direction":    {"type": "string", "maxLength": 4},
        "timestamp":    {"type": "string"}
    }
}
