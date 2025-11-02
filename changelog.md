## 0.4.0

- Renamed `LedgerType.PRESENT` to `LedgerType.CURRENT`.
- Added a `parse_timestamp` helper to parse string timestamps into Unix epoch ints
- Added nullable `Entry.timestamp` column to make querying easier.
- `Customer` and `Vendor`: `details` column is now a packify.SerializableType
  stored as a blob.
- Bug fix: `Entry.insert_many()` and `ArchivedEntry.insert_many()` did not
  function and had been skipped in tests. They now work as expected and are
  covered by e2e test suite.

## 0.3.3

- Added text `description` column to the following models:
  - `Account`
  - `ArchivedEntry`
  - `ArchivedTransaction`
  - `Currency`
  - `Customer`
  - `Entry`
  - `Identity`
  - `Ledger`
  - `Statement`
  - `Transaction`
  - `Vendor`
- Corrected `Customer` and `Vendor`: `details` column was incorrectly handled as
  a packify.SerializableType stored as a blob, but the column type was text.
  This has been corrected, and a note has been added to the documentation to
  indicate that this will be changed to a packify.SerializableType stored as a
  blob in 0.4.0.
- Small improvements to some documentation

## 0.3.2

- Updated packify dependency to 0.3.1 and applied compatibility patches
- Small changes to documentation

## 0.3.1

- Updated `Currency`:
    - Added `from_decimal` method
    - Updated `format` method to include non-decimal formatting,
      e.g. 'H00:00:00'

## 0.3.0

- Added `Statement`, `ArchivedTransaction`, and `ArchivedEntry`
- Updated `Transaction`: added `archive` method
- Updated `Account`:
    - Added `archived_entries` relation
    - Updated `balance` method to accept `previous_balances` parameter
- Updated `Entry`:
    - Added `archive` method
- Updated `Ledger`:
    - Added `archived_transactions` relation
    - Added `statements` relation

## 0.2.3

- Patch: readme links pointed to outdated documentation

## 0.2.2

- Patch: updated sqloquent dependency
- Updated `Account`: added boolean `active` column
- Added `get_migrations` tool
- Updated `publish_migrations` to accept callback to modify migrations

## 0.2.1

- Patch: expose `LedgerType` at module level

## 0.2.0

- Adapted bookchain v0.2.0 update: new `AccountCategory` and `LedgerType`
- Added a few helpful methods
