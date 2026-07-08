## Context
All the data required for this challenge is contained within a single Excel file with multiple sheets. This is a 2-stage challenge.

## Requirements
- Input the data
- Bring the Animal & Plant Details Tables together to form one table
  - There's been an error in the Plant Details table where the Status field has been incorrectly spelt as Stattus. Be sure to make sure these 2 fields align and have the correct spelling for their field name
  - Make sure the Animal and Plant fields from their respective tables are also aligned. Call this new field Name
- We only wish to keep the Name, Table Names, Status and Class fields for our analysis
- Use the Table Names field to extract the information of whether each row of data is an Animal or a Plant. Call this new field Wildlife
- Many of the Class names have the Latin name followed by the English name in brackets. Update the Class field so that it contains the English name, where possible (e.g., Aves (Birds) should become Birds)
- Combine this data with the Wildlife Table
  - All animals and plants should exist in both tables so we're expecting to still have 326 rows
  - There's an issue that needs to be fixed to achieve this. Some Names in the Wildlife Table have an error where the apostrophe's (') have been encoded as ' (e.g., Bird's-nest Fern should be Bird's-nest Fern)
- Remove any unnecessary fields
- Reduce the San Diego Climate Table to a single row which describes the temperature range in San Diego (you may choose to work in either Fahrenheit or Celsius)
- Append this data onto the Stage One Output
- Some Wildlife can exist in multiple Habitats. In our dataset these different habitats are separated by commas. Transform the data so that we have a row per Habitat for each Wildlife Species
- From the Habitats (estimates) Table, extract the information about the temperature ranges for each Habitat
- Combine the tables
- Reduce the dataset down to a single row per Wildlife Species, with the minimum and maximum temperatures they live in in the wild
- Create 2 calculated fields:
  1. Habitat Notes - classifies whether the animal is within its natural temperature range or not (Ideal = within temperature range of habitat; Above = San Diego is sometimes hotter than its habitat; Below = San Diego is sometimes colder than its habitat)
  2. Degrees outside Ideal - if the wildlife is not in their ideal temperature range, the number of degrees San Diego can be above or below the ideal temperature range
- Filter the data to only those who are not in their ideal temperature range
- Create the Priority Order:
  - Bring in the Care Priority lookup table (be careful not to lose any wildlife; if a wildlife species doesn't have a Status, make their Priority number 6)
  - Take the absolute value of the Degrees outside Ideal field
  - Create the ranking as described above, called Priority Order (if a wildlife species doesn't have a Status, make sure the Priority Order is also null)
- Remove unnecessary fields
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Wildlife
    - Name
    - Class
    - Region
    - Habitat
    - Status

- output_02.csv
  - 9 fields:
    - Wildlife
    - Name
    - Priority Order
    - Habitat Notes 
    - Degrees outside Ideal
    - Status
    - Class
    - Region
    - Habitat
