    Feature Backend health
    Simple health check for the backend

    Background: Server available
        Given server available

    Scenario: Server heart is working
        When GET "/" route
        Then message contains "HEALTHY"
        And response code is 200
