Feature: TripPlanning — turn a decided trip into a structured plan and learn from it

  Scenario: Plan an already-decided trip
    Given a Trip to "Norman's house" for 3 named travellers in "family visit"
    When I export the Plan Request
    Then the file matches plan-request.schema.json and bundles every Travel Note
      whose scope (household, this kind, a traveller, or this destination) applies

  Scenario: Import a plan and pack from it
    When I import a valid Trip Plan file
    Then the Packing List is interactive (check off items, see who each is for)
      and the other sections render as read-only titled prose

  Scenario: Debrief captures knowledge
    Given a Trip whose end date has passed
    When I complete the Debrief (what worked / missing / remember)
    Then each answer is saved as a Travel Note with a confirmable scope
