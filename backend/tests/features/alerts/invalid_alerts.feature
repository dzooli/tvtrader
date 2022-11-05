Feature Normal invalid alerts

Background: Server is running
    Given server available

@alert_invalid
Scenario Outline: Invalid alert - missing interval
    Given alert with <id>, <name>, <symbol>, <interval>, <direction>, <price>, <timestamp>
    And  interval:n field is missing 
    When sending the prepared alert
    Then response code is 400

    Examples:
    | id | name | symbol | interval | direction         | price | timestamp            |
    | 1  | STR1 | GBPUSD | 1        | BUY               | 1.1   | 2022-11-04T15:55:57Z |

@alert_invalid
Scenario Outline: Invalid alert - invalid interval
    Given alert with <id>, <name>, <symbol>, <interval>, <direction>, <price>, <timestamp>
    And  interval:n field is invalid
    When sending the prepared alert
    Then response code is 500

    Examples:
    | id | name | symbol | interval | direction         | price | timestamp            |
    | 1  | STR1 | GBPUSD | 1        | BUY               | 1.1   | 2022-11-04T15:55:57Z |
