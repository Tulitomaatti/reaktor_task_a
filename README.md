# Reaktor summer job application task

* "Sovellus, jonka avulla käyttäjät pääsevät helposti perehtymään hiilidioksidipäästöjen kehittymiseen viimeisten vuosien aikana."
* 

## Data 

* CSV: http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv 
* CSV: http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=csv

## Product

* Mobile or laptop: browser based solution. 
* API for data access 
* Minimize active maintenance tasks (e.g. data updates)

## Feature suggestions: 

[ ] CO2 per capita
[ ] Sorting 
[ ] Hilight superpowers vs. other countries 
-> Multiple series simulatenously, possible aggregates. 

[ ] Time range selector 

## UI

Title, searchbox, graph. 

* Checkboxes or radio buttons for extra features? 
* Button to remove series? Add series when selected from search? 

## Thoughts

Sounds like setting up a time series database (influxdb?) with a Grafana(-like) front sounds like a good idea on the long run.
 
A nice CSV parser coupled with a plotting library (plotly?) and something to handle data nicely (numpy, scipy, pandas?) would be the relevant choice here. Dash came up when googling for plotting and dashboards. 
