## Context

Simulate the NBA Draft Lottery to assign draft positions for the 14 non-playoff teams. The lottery determines the first four picks via predefined odds and predetermined winning numbers; picks 5–14 are assigned by original seed order.

You are provided with:
- **Lottery Odds**: odds by seed (1–14) for each of the first four picks, with separate probability columns `1`, `2`, `3`, and `4`.
- **Lottery Combinations**: a scaffold representing the 1,000 possible lottery outcomes (numbers 1–1000). This can be treated as the ordered integers 1–1000 for mapping purposes.
- **Team Seeding**: the 14 teams and their original seeds.

## Requirements

- Input the data.
- Treat seeds as ordered from lowest to highest numeric value (Seed 1 through Seed 14) when constructing any cumulative allocations.
- For each of the first four picks, construct an independent mapping from the 1,000 lottery numbers (1–1000) to seeds using that pick’s odds column:
  - Pick 1 uses odds column `1`; pick 2 uses column `2`; pick 3 uses column `3`; pick 4 uses column `4`.
  - Convert each seed’s percentage for that pick into an integer count of lottery numbers out of 1,000, ensuring the counts sum to exactly 1,000:
    - Compute the raw (non-integer) allocation as `(percent / 100) * 1000`.
    - Take the floor of each raw allocation.
    - Distribute any remaining numbers (to reach a total of exactly 1,000) to the seeds with the largest fractional remainders; break ties by seed order (lower seed number first).
    - (If the floored totals ever exceed 1,000, remove numbers from seeds with the smallest fractional remainders; break ties by seed order.)
  - Build the number-to-seed mapping by assigning each seed a contiguous block of lottery numbers in ascending seed order, with block sizes equal to the computed integer counts (so the mapping is a length-1,000 sequence where position 1 corresponds to lottery number 1, etc.).
  - Note: Teams/seeds are not removed between picks 1–4; each pick is evaluated independently against its own column of odds.
- Use the following predefined winning numbers to determine the winners for picks 1–4 by looking up the corresponding seed in that pick’s independent mapping:
  - Pick 1 → winning number: `282`
  - Pick 2 → winning number: `95`
  - Pick 3 → winning number: `378`
  - Pick 4 → winning number: `48`
- Attach the team name for each selected seed using the Team Seeding input (match on seed).
- Allocate the remaining picks (5–14) by original seed order (1 through 14), regardless of whether a team appeared in picks 1–4:
  - Pick 5 corresponds to seed 1, pick 6 to seed 2, …, pick 14 to seed 10 (continuing in ascending seed order until picks 5–14 are filled).
  - For each of these rows, attach the corresponding team name via the Team Seeding input.
- Produce a single output table with one row per actual pick (1 through 14), containing the actual pick number, the original seed assigned to that pick, and the associated team name. Keep rows ordered by `Actual Pick` ascending.
- Output the data.

## Output

- output_01.csv
  - 3 fields:
    - Actual Pick
    - Original
    - Team