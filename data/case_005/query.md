## Context

Hands-up all of you who have a system in your organisation that let's your team enter free text answers in to a system? Ok, well that's most of you and I feel for each and every data guru that sits at the end of the database where that information is stored. If you didn't put your hand up, you will have a lot to learn this week!

I have often wondered whether I would have a career if it wasn't for projects delivering new operational systems not considering that the 'Junk In' to 'Junk Out' rule is a very pertinent one. Project budget cuts, lack of data awareness and time constraints all lead to a perfect storm of project delivery challenges. One of the side-effects of this is felt as soon as the project releases; how is the new system performing and is it doing what we expected? Welcome to this week's challenge!

The input for this week's data is from a small financial services company's contact centre who have to measure some key statistics like: Number of Balances that are being requested, Number of Statements being asked for, Number of complaints being raised. We need to know those numbers by Policy Number and Customer ID so we can see who is using the call centre to hopefully get them on to our website instead to self-service. When are our busiest days for the contact types above? The data set we are asking you to create will allow you to load that in to Tableau to get those answers - create a viz if you want to!

## Requirements

- Input the data
- Create a date per day
- Determine how the customer contacted the company
- Create a separate column for the Policy Number
- Remove contacts that don't have a Policy Number
- Identify whether the contact was about a balance check, getting a statement or raising a complaint
- Get rid of unrequired columns
- Output the data

## Output

- output_01.csv
  - 6 fields:
    - Statement?
    - True Date
    - Balance?
    - Complaint?
    - Policy Number
    - Customer ID
