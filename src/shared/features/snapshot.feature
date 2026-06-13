Feature: Cross-cutting — snapshot sync (ADR-0002)

  Scenario: Snapshot sync
    When I export a snapshot on device A and import it on device B
    Then device B holds the same data (whole DB, schema-versioned; last import wins)
