# Rationale

I used the 80 Cereals dataset (from kaggle.com) because I wanted a simple nutrition table I could actually filter. The question I care about is whether cereals with more sugar get a worse rating, and whether that looks different by brand.

One limit is that sugars and a few other columns use -1 for missing values. That is not a real sugar amount, so the slider and the scatter can look a little off unless you notice it. 

The two metrics are "cereals shown" and "average rating." Both come from the filtered table, not from a number I typed. The count tells you if the filters left anything. The average rating tells you if the cereals that remain are rated better or worse, which matches the sugar vs rating question.

I used an Altair bar chart of average rating by manufacturer because I needed a grouped number, not one bar per cereal. A bar is the straightforward way to compare brands. I used a Plotly scatter of sugars vs rating because each cereal is one point and you can see the drop in rating as sugar goes up. Hover shows the name. Both charts use filtered, so they change when the widgets change.

