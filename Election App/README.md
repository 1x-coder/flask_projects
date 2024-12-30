# 2023-election-app


> Web app that visualizes the votes distribution of the 2023 Polish parliamentary election.

https://github.com/h4em/2023-election-app/assets/72524655/f1e38003-9a9a-4eb4-82c1-d0586c17eac8

<a name="mobile-preview"></a>

https://github.com/h4em/2023-election-app/assets/72524655/553669c8-a649-4309-bdbe-0e4353b90fde

## About 
This repo showcases a simple web-app project I've made on the side. It's all about visualising the 2023 Parliamentary election data available @[wybory.gov.pl/sejmsenat2023/](https://wybory.gov.pl/sejmsenat2023/pl/dane_w_arkuszach).

## Tech used
<p align="center">
  <img src="https://user-images.githubusercontent.com/25181517/192158954-f88b5814-d510-4564-b285-dff7d6400dad.png" alt="HTML" width="48" height="48" style="margin-right: 16px;">
  <img src="https://user-images.githubusercontent.com/25181517/183898674-75a4a1b1-f960-4ea9-abcb-637170a00a75.png" alt="CSS" width="48" height="48" style="margin-right: 16px;">
  <img src="https://user-images.githubusercontent.com/25181517/117447155-6a868a00-af3d-11eb-9cfe-245df15c9f3f.png" alt="JavaScript" width="48" height="48" style="margin-right: 16px;">
  <img src="res/jquery.svg" alt="JavaScript" width="48" height="48" 
  style="margin-right: 16px;">
  <img src="res/chartjs.png" alt="chartjs" width="48" height="48" 
  style="margin-right: 16px;">
  <img src="res/leafletjs.png" alt="leaflet" width="48" height="48" 
  style="margin-right: 16px;">
  <img src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" width="48" height="48" style="margin-right: 16px;">
  <img src="https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png" alt="Flask" width="48" height="48" style="margin-right: 16px;">
  <img src="res/pandas.svg" alt="pandas" width="48" height="48" 
  style="margin-right: 16px;">
  <img src="res/sqlalchemy.svg" alt="sqlalchemy" width="48" height="48" 
  style="margin-right: 16px;">
  <img src="https://user-images.githubusercontent.com/25181517/183896128-ec99105a-ec1a-4d85-b08b-1aa1620b2046.png" alt="MySQL" width="48" height="48" style="margin-right: 16px;">
</p>

<!-- <p>
    img sources
    https://github.com/marwin1991/profile-technology-icons
    https://simpleicons.org/?q=connector
</p> -->

## How it works
- The user searches for a place name via the searchbar with categories to choose from: 'Address', 'City', 'Gmina', 'Powiat', 'Wojewodztwo' and gets nice charts in return. 
- The place location is visualised on a map. 
- Note that lookup for category 'Address' provide results for the **exact building** in which the voting took place, so for e.g 'Szkola Podstawowa xxx' ([see here](#mobile-preview)). 
- Data from **abroad** / **ships** was **excluded**.

## How it's made
- I downloaded the original .csv files and parsed them to make a relational database. Used Pandas and MySQL, [see the ERD here](res/entity-relationship-diagram.png). 
- [/data/](/data/) directory is where i do the parsing / database insertions with SQLAlchemy.
- Made a Flask server with endpoints that enable looking up places and their corresponding voting results, again, used SQLAlchemy and AJAX for this.
- Used [Nominatim API](https://nominatim.org/) for place location and GeoJSON data fetching, which is then represented on a [Leaflet](https://leafletjs.com/) map.
- Used [Chart.js](https://www.chartjs.org/) for charts.
- Made it somewhat responsive with CSS Flexbox.

## Data integrity
Here are some screenshots comparing my results with the official ones. For majority of cases they should check out.
<p align="center">
  <img src="res/res-comp-wwa.png" alt="wwa" height="512px">
  <img src="res/res-comp-sowin.png" alt="sowin" height="512px">
</p>
<p align="center">
  <img src="res/res-comp-lomianki.png" alt="lomianki" height="512px">
  <img src="res/res-comp-plock.png" alt="plock" height="512px">
</p>
