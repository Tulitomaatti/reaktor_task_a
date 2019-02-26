# Reaktor summer job application task

* "Sovellus, jonka avulla käyttäjät pääsevät helposti perehtymään hiilidioksidipäästöjen kehittymiseen viimeisten vuosien aikana."

## Afterthoughts

Nice intro to Dash/Plot.ly and Heroku. The implementation is largely based on reading Dash and Plot.ly documentation and adapting them to build a CO2 emission explorer app. 

The specifications also ask for an API to fetch data from the app in order to implement future UI's. This feels a bit out of place, as most of the app is about extracting the data from an already working API at World Bank. On the other hand setting up a database for this seems a bit overkill as well. Building functionality to access cleaned data via Flask might be one answer, but even that feels like reinventing the wheel, a wheel that's worse than existing solutions.  

The current application fetches fresh data from World Bank when started up; a restart every year or so should keep the data up to date, given that World Bank does not change the format they server data in. 

## Data 

* CSV: http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv 
* CSV: http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=csv

## Product

* Mobile or laptop: browser based solution. 
* API for data access 
* Minimize active maintenance tasks (e.g. data updates)

## Feature suggestions: 
- [x] CO2 per capita. (= some mode selector.)
- [ ] Sorting 
- [x] Hilight superpowers vs. other countries (= multiple series displayed simulatenously).

## UI

Title, searchbox, graph. 

* Checkboxes or radio buttons for extra features? 
* Button to remove series? Add series when selected from search? 

## Thoughts

Sounds like setting up a time series database (influxdb?) with a Grafana(-like) front sounds like a good idea on the long run.
 
A nice CSV parser coupled with a plotting library (plotly?) and something to handle data nicely (numpy, scipy, pandas?) would be the relevant choice here. Dash came up when googling for plotting and dashboards. 

## TODO

- [x] Fetch data
- [x] Parse data into a sensible structure
- [x] Figure out how to draw a plot
- [x] Figure out how to make a search box
- [x] Make plot interactive
- [x] Timescale slider
- [x] Add plotting features: stacking, diffs, per capita.
- [x] Tidy up layout
- [x] Package and test
- [x] Finish application. 
