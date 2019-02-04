Feature: Generate scenarios input using hypothesis

Scenario: test if the inverse of the square equals the argument
Given we have a float number
When we square it
And we take the root
Then the result equals the original argument
