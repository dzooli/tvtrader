    Feature Backend health
    Simple tests for the Backend

    Background: Server available
        Given server available

    Scenario: Server heart is working
        When GET "/" route
        Then message contains "HEALTHY"
