## Context
In market basket analysis, we need to calculate three key metrics: support, confidence, and lift. We calculate these metrics for individual items and for association rules between items.

An **association rule** is a statement about two items (or two sets of multiple items) which says “if customers buy X, they also buy Y”. This is generally written out like “X → Y”. For example, the association rule “moisturiser → hand soap” describes the situation where customers buy moisturiser, and they also buy hand soap. This is sometimes read aloud as “Y, given X” - or “customers buy hand soap, given the fact that they’re buying moisturiser too.

The **support** for an item (or set of items) is a simple fraction - it’s the number of times an item is bought out of the total number of transactions. So, the support for hand soap is 0.6; it turns up in 3 transactions, and there are 5 transactions in total.

The **confidence** for an association rule depends on the direction of the association rule. Confidence is the support for the right hand side of the rule out of all transactions which contain the left hand side of the rule. So, if the association rule is “moisturiser → hand soap”, then the confidence for that rule is the number of transactions containing moisturiser which also contain hand soap (which is 3) out of the number of transactions containing moisturiser (which is 4). That’s 0.75. This is why the direction of the association rule is important - if the rule is “hand soap → moisturiser”, then the confidence is 1, because all three transactions containing hand soap also contain moisturiser.

Finally, **lift**. Lift is how many more (or fewer) transactions there are which contain both items than you’d expect if there was no relationship between the two and people just put items into their baskets at the rate of support for each item. The support for moisturiser is 0.8 and the support for hand soap is 0.6. If there was no relationship between the two, then the number of transactions containing both items should be 0.6 * 0.8, which is 0.48 … or in other words, if 80% of people buy hand soap and 60% of people buy moisturiser, then just under half of people should buy both. But that’s not what we’ve got! In fact, 60% of transactions contain both hand soap and moisturiser. That’s 25% more often than you’d expect. This means that the lift for moisturiser and hand soap is 1.25, because 1.25 more transactions contain both items than you’d expect given their individual support (because 0.6 / 0.48 = 1.25). Another way of calculating lift is taking the confidence of the right hand side given the left hand side (so, for “moisturiser → hand soap”, that’s is 0.75), and divide that by the support for the right hand side (so, that’s support for hand soap, which is 0.6). 0.75 / 0.6 = 1.25. Lift can also be negative - not numerically negative, but expressing reduced probability. For example, people who go to the supermarket and buy tofu are probably not going to buy rich beef sausages. If 20% of people buy tofu and 20% of people buy rich beef sausages, you’d expect an overlap of 4% of people buying both if there’s no relationship between the two … but it may well be more like only 1% of people. That’s a lift of 0.25, which means that people buy those products together only 0.25 as much as you’d expect if there was no relationship between the items.

In this week’s challenge, we’re only going to calculate the metrics for one-to-one association rules between individual items, like “moisturiser → hand soap”. In the real world, you’d work with one-to-many, many-to-one, and many-to-many association rules as well, like “moisturiser → {hand soap, razors}” and “{moisturiser, razors} → {hand soap, shaving cream}.

## Requirements
- Input the data
- Transform the data set so that each transaction and item has its own line (but keep a field with the original comma-delimited transaction list - it’ll be useful later).
- Calculate support for each item.
  - The new LOD functionality in Prep 2020.1 is really handy here.
- Create association rules between each item by putting an arrow in between each item pair (I just used “-->”, but feel free to use the ASCII arrow of your choice).
  - Hint: You’ll also want to make sure that you’re not creating impossible association rules - e.g. “hand soap → hand soap” is impossible because it’s the same item, and “razors → bath bomb” is impossible because those two items never get bought together in this data set.
- Calculate support for the RHS items given the LHS items. This is where having the full comma-delimited transaction list comes in handy.
  - Hint: this is another great place for the new LOD functionality.
- Calculate the confidence for the association rules.
- Now that you’ve got the support and confidence, you can use those together to calculate the lift for each association rule.
  - Hint: I prefer thinking about lift calculations by using ([support for both items])/([support for LHS item] * [support for RHS item]) because it’s clearer to me conceptually how it works, but I found that it was easier to calculate it in my flow by using ([confidence for association rule] / [support for RHS item])
- Output the data

## Output

- output_01.csv
  - 7 fields:
    - AssociationRule
    - LHSItem
    - RHSItem
    - LHS Support
    - RHS Support
    - Confidence
    - Lift
