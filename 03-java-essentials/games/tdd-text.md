| Cycle | Test written (red) | Minimal change to go green | Refactor notes  |
| ----- | ------------------ | -------------------------- | --------------- |
| **1**                 | “Hey, are you free tonight?” → ✅ SEND                                     | None; naive system already passes     | Baseline established                                        |
| **2**                 | “We need to talk.” → 😬 MAYBE DON'T                                       | Detect exact phrase “we need to talk” | Don't generalize yet                                        |
| **3**                 | “I had a dream about you last night.” → 😬 MAYBE DON'T                    | Detect “I had a dream about you”      | Awkwardness rule is intentionally narrow                    |
| **4**                 | “I know what you did.” → 🚨 DELETE YOUR PHONE                             | Detect “I know what you did”          | Introduced highest-severity result through the failing test |
| **5**                 | “If you receive this message, pretend you didn't.” → 🚨 DELETE YOUR PHONE | Detect “pretend you didn't”           | Still no broad rule engine                                  |
| **6 — Refactor only** | —                                                                         | —                                     | Consolidate the rules without changing behavior             |
