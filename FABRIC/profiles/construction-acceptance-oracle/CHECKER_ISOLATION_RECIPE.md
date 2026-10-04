# Oracle CHECKER isolation recipe (fresh/read-only)
1. same frozen Oracle Distribution digest as the COMMANDER
2. fresh session or ephemeral checker run (no commander session reuse)
3. maker memory preload OFF
4. candidate/source/evaluator write tools ABSENT
5. authority/promotion tools ABSENT
6. allowed write-set = OracleReceipt + checker logs only
7. output = OracleReceipt only (schema RP002-ORACLE-RECEIPT/1)
A same-profile long-running session that previously commanded the maker is NOT sufficient.
