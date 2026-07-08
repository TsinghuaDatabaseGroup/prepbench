## Context

It's time for another collaboration with #GamesNightViz! Over the last few months, the #GamesNightViz team have been playing Elden Ring which has inspired this challenge. We’re looking for the highest damaging weapons we can use throughout our playthrough. Using data tables from we have the base stats for all the melee weapons however, it’s a little messy! The goal is to create an output of the highest damaging weapon by its required level.

## Requirements

- Input the data
- Load the dataset
- Split the dataset into two tables
  - Damage Stats: 1 containing: Name, Category, Phy, Mag, Fire, Ligh, Holy
  - Level Requirements: 1 containing: Name, Str, Dex, Int, Fai, Arc
- For Damage Stats, if you look at the data in Phy, Mag, Fire, Ligh, Holy:
  - the first value shows the attack damage
  - the second value shows the damage resistance
  - A dash “-” means 0, i.e. no damage
- For Level Requirements, for Str, Dex, Int, Fai, Arc:
  - the first value shows the level required
  - the second value shows the weapon scaling rating
  - A dash “-” means 0, i.e. no requirement or scaling
- Pivot the two datasets:
  - For Damage Stats,1 column containing Phy, Mag, Fire, Ligh, Holy and 1 for the values
  - For Level Requirements,1 column containing Str, Dex, Int, Fai, Arc and 1 for the values
- Split the pivot values into 2 columns for both tables:
  - For Damage Stats label the first column “Attack Damage”, and the second “Damage Resistance"
  - For Level Requirements label the first column “Required Level”, and the second “Attribute Scaling"
- Replace the “-” values with zero in the columns: “Attack Damage”, “Damage Resistance”, “Required Level” and change the datatype to whole numbers (integer)
- Find the total “Attack Damage” and total “Required Level” for all weapons and join the datasets together.
- Rank the weapons by total attack damage, grouped by the total required attribute.
- Filter for the number 1 rank and output the data
- Output the data

## Output

- output_01.csv
  - 4 fields:
    - Name
    - Category
    - Required Level
    - Attack Damage
