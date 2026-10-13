# Validation and rollback

| change class | positive test | negative test | rollback |
|---|---|---|---|
| mirror content refresh | the new commit's tree contains exactly the intended paths, and the manifest's published set equals the tree | a path absent from the approval list must not appear in the tree | revert the commit (`git revert`) or reset the ref to the previous SHA |
| manifest edit | JSON parses; declared exclusions equal the measured published set | a declared exclusion that is still present in the tree fails the change | restore the previous manifest blob |
| generated-file removal (`.pyc`, `.lnk`) | after the change the count of matching blobs is 0 | a removal affecting a non-generated path fails the change | restore the removed blobs from the previous tree |
| publish-control file | root `.gitignore` exists and its patterns are the intended ones | a pattern that would exclude an approved publication path fails the change | delete the file |
| document set | every file in `INTEGRATION/README.md`'s table exists and parses | a referenced artifact that does not exist fails the change | delete the added documents |

Every row is falsifiable from the repository alone: counts come from the tree listing, not from prose.
