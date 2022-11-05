Feature Normal invalid alerts

Background: Server is running
    Given server available

@alert_invalid
Scenario Outline: Invalid alert - missing or invalid fields
    Given alert with 1, STRAT1, GBPUSD, 1, BUY, 1.2, 2022-11-04T15:55:57Z
    And  <field> field is missing 
    When sending the prepared alert to endpoint: <endpoint>
    Then response code is <code>

    Examples:
    | field        | miss_or_inv | code | endpoint     | 
    | id:n         | missing     | 400  | alert        |
    | name:s       | missing     | 400  | alert        |
    | symbol:s     | missing     | 400  | alert        |
    | interval:n   | missing     | 400  | alert        |
    | direction:s  | missing     | 400  | alert        |
    | price:n      | missing     | 400  | alert        |
    | timestamp:s  | missing     | 400  | alert        |
    | id:n         | invalid     | 400  | alert        |
    | name:s       | invalid     | 400  | alert        |
    | symbol:s     | invalid     | 400  | alert        |
    | interval:n   | invalid     | 400  | alert        |
    | direction:s  | invalid     | 400  | alert        |
    | price:n      | invalid     | 400  | alert        |
    | timestamp:s  | invalid     | 400  | alert        |
    | id:n         | missing     | 400  | carbon-alert |
    | name:s       | missing     | 400  | carbon-alert |
    | symbol:s     | missing     | 400  | carbon-alert |
    | interval:n   | missing     | 400  | carbon-alert |
    | direction:s  | missing     | 400  | carbon-alert |
    | price:n      | missing     | 400  | carbon-alert |
    | timestamp:s  | missing     | 400  | carbon-alert |
    | id:n         | invalid     | 400  | carbon-alert |
    | name:s       | invalid     | 400  | carbon-alert |
    | symbol:s     | invalid     | 400  | carbon-alert |
    | interval:n   | invalid     | 400  | carbon-alert |
    | direction:s  | invalid     | 400  | carbon-alert |
    | price:n      | invalid     | 400  | carbon-alert |
    | timestamp:s  | invalid     | 400  | carbon-alert |
