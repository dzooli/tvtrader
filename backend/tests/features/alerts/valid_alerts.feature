Feature Normal valid alerts

Background: Server is running
    Given server available

@alert
Scenario Outline: Valid alerts
    Given alert with <id>, <name>, <symbol>, <interval>, <direction>, <price>, <timestamp>
    When sending the prepared alert to endpoint: <endpoint>
    Then response code is 200
    And message contains "OK"

    Examples:
    | id | name | symbol | interval | direction         | price | timestamp            | endpoint     |
    | 1  | STR1 | GBPUSD | 1        | BUY               | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | buy               | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | SELL              | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | sell              | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | Close long        | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | Close short       | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | Close short entry | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | Close long entry  | 1.1   | 2022-11-04T15:55:57Z | alert        |
    | 1  | STR1 | GBPUSD | 1        | BUY               | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | buy               | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | SELL              | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | sell              | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | Close long        | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | Close short       | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | Close short entry | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |
    | 1  | STR1 | GBPUSD | 1        | Close long entry  | 1.1   | 2022-11-04T15:55:57Z | carbon-alert |


