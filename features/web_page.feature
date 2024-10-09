Feature: Bank Manager Customer Management
    Scenario: Add and Delete a Customer
        Given I am on the Bank Manager Login page
        When I log in as a Bank Manager
        And I add a customer with "John" as first name, "Smith" as last name and "12345" as postcode     
        When I search for the customer "John" in the customers list
        Then I should see "John Smith" in the customers list
        When I delete the customer "John"
        Then I should not see "John Smith" in the customers list