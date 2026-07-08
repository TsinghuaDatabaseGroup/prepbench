## Context
The cards need to be sorted as follows:
- Based on which gym leader they belong to
- In the order of the Kanto gyms
- With the Gym Leader card first
- Followed by their Gym card
- Followed by the remaining Trainer cards associated with them (in card number order)
- Followed by their Pokémon in Pokédex order
- Using the Pokémon level in the bottom left corner of the card, where a leader has multiple of the same Pokémon
- With leftover trainer cards not associated with a leader at the end (in card number order, with the Gym Heroes set coming before the Gym Challenge set where there are ties)

## Requirements
- Input the 4 csv files
- For the Pokémon Cards Input, separate the Gym Leader and Pokémon (e.g. Blaine's Vulpix becomes Blaine and Vulpix in separate fields)
- Use the Pokémon Input to bring in information about the Pokédex Number (make sure not to duplicate any rows)
- Combine with the Trainer Cards Input
- Use the Table Names field to identify the Card Type, either Pokémon or Trainer
- Any rows that do not have a Leader, assign as "Leftover Trainers"
- Combine with the Leader Order Input
- Based on the above description, find a way to sort the cards into the correct order
- Remove unnecessary fields
- Output the 1 csv file

## Output

- output_01.csv
  - 6 fields:
    - Sort Order
    - Leader
    - Gym Set
    - Number
    - Card
    - Card Type
