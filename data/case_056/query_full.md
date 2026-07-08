## Context

C&B Suds Co has four end-of-day orders that were written down as disconnected notes: the set of customer titles, last names, products ordered, and priority positions are all known, but the correct one-to-one matching between these attributes is unknown. Your task is to reconstruct the single consistent set of four customer orders by applying the provided logic clues, without guessing.

## Requirements

- Input the data  
  We’re offering two possible starting points for this challenge: one input has the data pre-prepared with all possible combinations of the four fields, and one where you have to produce this yourself. Use the former input if you want to jump right into solving the logic grid puzzle part of the challenge! In the raw input, the row position of each value in each field is arbitrary as we currently don't know how they should actually be arranged. We'll also advise that there may be other ways to accomplish this task but we hint at the method we use in the requirements below and in the format of the pre-prepared data. We used version 2019.3.2 in building the challenge.  
  - Pre-prepared data.  
  - Raw data.

- If the data hasn’t been prepared then prepare it so there is a row for every [Title], [Last Name], [Product], and [Priority] combination.  
  This prepared dataset should represent the full Cartesian product of the four attribute lists (i.e., each row is one candidate assignment of a single Title + Last Name + Product + Priority).

- Solve the logic grid by applying the clues as constraints to identify the single valid assignment consisting of exactly 4 final rows (one per customer), where:
  - Each of the four last names appears exactly once, each title appears exactly once, each product appears exactly once, and each priority value (1–4) appears exactly once.
  - All clues below are satisfied simultaneously:

  1. Only the customer with the highest priority (Priority = 1) has a title and last name that begin with the same letter. No other priority can have matching initials between Title and Last Name.
  2. Bevens’ priority is exactly one position after Dimmadome’s priority. Additionally, neither Bevens nor Dimmadome ordered the Chamomile Bar or the Hibiscus Soap-on-a-Rope.
  3. The Sergeant’s priority must be either 1st or 3rd. Separately, the person who ordered Lemon Gel must also have priority either 1st or 3rd.
  4. The Reverend did not order the Rose Bar and is not 2nd priority.
  5. The Sergeant either ordered Hibiscus Soap-on-a-Rope or is 4th priority. Given clue 3 restricts the Sergeant to priorities {1, 3}, this implies the Sergeant must have ordered Hibiscus Soap-on-a-Rope.
  6. The priority of the person who ordered the Rose Bar is exactly one position after the priority of the person who ordered the Lemon Gel (Priority(Rose Bar) = Priority(Lemon Gel) + 1).
  7. Dimmadome is not a Doctor, and the Baroness did not order Hibiscus Soap-on-a-Rope.

- Using the Profile Pane or otherwise, filter the data using the clues above.  
  Apply any constraints that can be enforced row-by-row to reduce candidate combinations, then enforce the cross-row constraints (such as “directly after” relationships and the requirement that all titles/products/priorities are unique across the four final customers) to arrive at the single valid set of four orders.

- You do not need to make any guesses - the final outcome can be arrived at using logical deduction and the clues above!

- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Title
    - LastName
    - Product
    - Priority