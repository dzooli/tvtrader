    Feature Backend health
    Simple tests for the Backend

    Scenario: Server heart is working
        Given server available
        When GET "/" route
        Then message contains "HEALTHY"
