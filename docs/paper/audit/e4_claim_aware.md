# E4 rule-based claim-aware numeric audit

Claims extracted with entity/attribute/unit context; support searched in the query's tool observations.

| Variant | Claims | Direct | Attribute | Any number | Unsupported |
|---|---:|---:|---:|---:|---:|
| Multi-Agent (validation on) | 101 | 10.9% | 9.9% | 13.9% | 65.3% |
| Multi-Agent (validation off) | 96 | 16.7% | 6.2% | 13.5% | 63.5% |

**Interpretation and caveat.** `direct` requires the claim's entity and attribute to appear in the
tool observation and a value within 5%; `attribute` drops the entity requirement; `any_number` is
the old permissive criterion. Units are compared in the claim's canonical value without full
observation-unit parsing. This is a rule-based audit, not the human-labeled validation (E4);
it shows how much the permissive 0.444 score overstates claim-level support.
