## Context
You have weekly results from the quiz show *Richard Osman’s House of Games*. Officially, players earn points each day based on daily placement (1st=4, 2nd=3, 3rd=2, 4th=1), and Friday’s points are doubled. Weekly points determine the weekly winner.

Build a player-level output that compares the official weekly outcome to three alternative scoring approaches, and flags whether the weekly winner would change under each alternative.

## Requirements
- Input the data from `input_01.csv`.

- Keep only the fields required to compute weekly scores, weekly points, and ranks, and standardize naming to remove duplication:
  - `Ser.` becomes `Series`
  - `Wk.` becomes `Week`
  - `Total` becomes `Score`
  - the input’s weekly points field (labeled `Week`) corresponds to `Points`
  - the input’s weekly rank field (labeled `Week 1`) corresponds to `Rank`
  - (the day-label renames `T` → `Tu` and `T 1` → `Th` are only needed insofar as they help you consistently identify the daily score columns and Friday)

- Filter the data to remove rows where the Series identifier is missing/blank, or where the Series value begins with `N`. After filtering, `Series` must be treated as an integer series number.

- Define the grain of the output as **one row per Player per (Series, Week)**.

- Identify the five daily *placement* fields for Monday–Friday as the five columns immediately following the `Rate*` column. Convert placements into daily points using:
  - `1st` → 4
  - `2nd` → 3
  - `3rd` → 2
  - `4th` → 1

- Recompute weekly points from daily placements (do not rely on precomputed weekly points for these scenario calculations):
  - **Points without double points Friday** = sum of the five daily points (Mon–Fri), with no doubling on Friday.
  - **Points** (official double-Friday points) = `Points without double points Friday` + (Friday daily points).  
    (Equivalently, Friday points are counted twice while Mon–Thu are counted once.)

- Identify the five daily *score* fields for Monday–Friday as the five columns immediately preceding the `Total` column. Compute:
  - **Score** = the `Total` field as an integer.
  - **Score if double Friday** = `Score` + (Friday daily score).  
    (Equivalently, Friday’s score is counted twice while Mon–Thu are counted once.)

- Set **Original Rank** from the input’s official weekly rank field (the one described in the renaming step as `Week 1` → `Rank`). Parse out the numeric rank value (e.g., if the field contains a number embedded in a string, extract the digits). Use this as the reference “official” weekly ranking.

- For each (Series, Week), compute scenario ranks by ranking players **descending** on the relevant measure, using a tie method that assigns the minimum rank among tied players (i.e., tied leaders all get rank 1):
  - **Rank without double points Friday**: rank by `Points without double points Friday`
  - **Rank based on Score**: rank by `Score`
  - **Rank if Double Score Friday**: rank by `Score if double Friday`

- For each (Series, Week), compute whether the weekly winner changes under each scenario. Define:
  - Original winners = all players with `Original Rank` = 1 (may be multiple).
  - Scenario winners = all players with the scenario rank = 1 (may be multiple).
  - The “Change in winner … ?” flag is **True** if at least one original winner is **not** included among the scenario winners; otherwise **False**.  
    (If the scenario adds extra tied winners but still includes all original winners, that does **not** count as a change.)
  - Apply the same boolean flag value to every row within the (Series, Week) group.

- Remove unnecessary fields so the final dataset contains exactly the required 14 fields, with the specified names and order.

- Output the data.

## Output

- output_01.csv
  - 14 fields:
    - Series
    - Week
    - Player
    - Original Rank
    - Rank without double points Friday
    - Change in winner with no double points Friday?
    - Rank based on Score
    - Change in winner based on Score?
    - Rank if Double Score Friday
    - Change in winner if Double Score Friday?
    - Score
    - Points
    - Score if double Friday
    - Points without double points Friday