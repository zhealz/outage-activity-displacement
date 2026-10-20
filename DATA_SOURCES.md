# Data sources

All inputs are public. The notebooks download them at run time; none of the raw files are included here. The terms of use and citation requested by each provider apply.

## Power outages

**DOE EAGLE-I recorded electricity outages, 2014–2022** (Oak Ridge National Laboratory). Customers without power by county, every 15 minutes, from utility outage maps; zeros are not recorded.

- Record: [figshare 24237376](https://figshare.com/articles/dataset/The_Environment_for_Analysis_of_Geo-Located_Energy_Information_s_Recorded_Electricity_Outages_2014-2022/24237376)
- Files used: `eaglei_outages_2020` (figshare file 42547894), `eaglei_outages_2021` (42547891) and `coverage_history.csv` (42547714), downloaded from `https://ndownloader.figshare.com/files/<id>`; Step 1 also uses the 2022 and 2023 files (42547897 and 44574907)
- Used in: Step 1b (weekly hours without power per customer, event labels) and Step 1
- Citation: Brelsford, C. et al. (2024). A dataset of recorded electricity outages by United States county 2014–2022. *Scientific Data*, 11, 271. https://doi.org/10.1038/s41597-024-03095-5

The number of customers in a county is estimated as county population × statewide customers (from `coverage_history.csv`) ÷ state population.

## Human mobility

**GeoDS weekly county-to-county flows** (University of Wisconsin–Madison GeoDS Lab), derived from SafeGraph visit patterns: the number of visitors from one county to places in another, by week.

- Repository: https://github.com/GeoDS/COVID19USFlows-WeeklyFlows (`weekly_flows/county2county/`)
- Weeks used: the 48 distinct weeks covered by the eight events' 12-week windows in 2020–21, plus 8 weeks of September–October 2019 (56 files in all)
- Used in: Steps 1b to 5 (visits to places, residents' visits, outflow, network exposure). The 2019 weeks form a pre-pandemic network built in Steps 1 and 1b that later steps do not use; Steps 3 and 4 measure each county's usual ties from the event's own pre-storm weeks (−5 to −2)
- Citation: Kang, Y., Gao, S., Liang, Y., Li, M., Rao, J., & Kruse, J. (2020). Multiscale dynamic human mobility flow dataset in the U.S. during the COVID-19 epidemic. *Scientific Data*, 7, 390. https://doi.org/10.1038/s41597-020-00734-5

**BTS Trips by Distance** (Bureau of Transportation Statistics): daily trips and share of residents staying home, by county of residence. Socrata endpoint `https://data.bts.gov/resource/w96p-f2qv.csv`. Used in Step 1 and as a secondary measure in Step 1b.

## Businesses, workers and spending

**Opportunity Insights Economic Tracker**, files from https://github.com/OpportunityInsights/EconomicTracker (`data/`):

| File | Series | Placed by | Used in |
| --- | --- | --- | --- |
| `Womply - County - Weekly.csv` | Small-business revenue (`revenue_all`) and small businesses open (`merchants_all`), Womply | County where the business is | Steps 1, 1b, 2b, 5 |
| `Affinity - County - Daily.csv` | Card spending (`spend_all`), Affinity Solutions; 7-day moving average | County where the cardholder lives | Steps 1, 1b, 2b, 5 |
| `Employment - County - Weekly.csv` | Employees paid (`emp`, `emp_incbelowmed`, `emp_incabovemed`), Paychex; weeks end on Friday | County | Step 5 |
| `GeoIDs - County.csv` | County names and 2019 population | — | Steps 1b, 3, 4, 4b, 5 |

Values are changes from a base period (seasonally adjusted for Womply and Affinity); Step 5 converts them to log points from each county's pre-storm baseline. Counties with small samples are masked by the provider.

- Citation: Chetty, R., Friedman, J. N., Stepner, M., & the Opportunity Insights Team (2024). The economic impacts of COVID-19: Evidence from a new public database built using private sector data. *Quarterly Journal of Economics*, 139(2), 829–889. https://doi.org/10.1093/qje/qjad048

## Weather

Computed in Google Earth Engine (Step 2a), per county and week:

- **NOAA/NWS Real-Time Mesoscale Analysis** (`NOAA/NWS/RTMA`), hourly, 2.5 km: the week's highest hourly wind gust, averaged over the county (the county maximum is kept too)
- **PRISM daily** (`OREGONSTATE/PRISM/ANd`), PRISM Climate Group, Oregon State University, 4 km: weekly precipitation, wettest day, lowest temperature and frozen precipitation (precipitation on days with a maximum temperature of 2 °C or less); a PRISM day ends at 12:00 UTC
- County polygons in Earth Engine: `TIGER/2018/Counties`

## Places

- **County population (Step 1)**: Census Bureau county population estimates, `co-est2024-alldata.csv` (falling back to `co-est2023-alldata.csv`) from https://www2.census.gov/programs-surveys/popest/datasets
- **County boundaries**: Census Bureau cartographic boundary file 2020, `https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_500k.zip` (distances between counties, maps)
- **Coastline**: TIGER/Line 2020, `https://www2.census.gov/geo/tiger/TIGER2020/COASTLINE/tl_2020_us_coastline.zip`; Atlantic and Gulf segments only (Step 2c)
- **Median household income**: Census Bureau Small Area Income and Poverty Estimates 2019, `est19all.xls` from https://www.census.gov/data/datasets/2019/demo/saipe/2019-state-and-county.html (Step 5)
- **Rural–urban status**: USDA Economic Research Service, Rural-Urban Continuum Codes 2013 (codes 1–3 metro, 4–9 nonmetro), from https://www.ers.usda.gov/data-products/rural-urban-continuum-codes; the 2023 edition is a fallback in the code (Step 5)

## Event dates

Landfall or onset times come from the National Hurricane Center's Tropical Cyclone Reports (https://www.nhc.noaa.gov/data/tcr/), National Weather Service event summaries for the Iowa derecho (https://www.weather.gov/dvn/summary_081020) and the Oklahoma ice storm (https://www.weather.gov/oun/events-20201026), and the FERC–NERC preliminary findings on the February 2021 cold weather event (September 2021 presentation) for Winter Storm Uri.
