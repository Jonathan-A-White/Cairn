Feature: HomeInventory — capture and keep knowledge of where things are kept

  Scenario: Find by either family member's word
    Given an Item "dining cabinet" with alias "the hutch"
    When I search "hutch"
    Then the Item appears with its full Place path

  Scenario: Confirm a placement keeps it fresh
    Given a Placement of "stapler" in "office desk" last verified 30 days ago
    When I tap "Found it"
    Then last verified updates to now and records who verified

  Scenario: Correct a wrong placement
    Given a Placement of "stapler" in "junk drawer"
    When I tap "Actually at..." and pick "office desk"
    Then the stapler is placed in "office desk" and removed from "junk drawer"

  Scenario: Sweep a place quickly
    When I start a Sweep on "Attic -> eaves closet"
    Then I can rapid-add item after item without leaving the place

  Scenario: Photo-assisted sweep round-trip
    Given I exported a Sweep Request for "blue bin"
    When I import a valid Sweep Result file
    Then its items are shown for confirm/edit before being added to "blue bin"

  Scenario: Reject a malformed import
    When I import a JSON file that fails the schema
    Then nothing is written and I see a clear validation error
