# Time Series and Forecasting - Beginner Guide

## 1. What is Time Series Data?

A **time series** is a collection of observations recorded in **time order**.

The important difference between normal data and time-series data is that **time matters**.

For example:

```text
Date        Product Demand
----------  --------------
2026-01-01       100
2026-01-02       110
2026-01-03       115
2026-01-04       108
2026-01-05       120
```

Here, the demand values are not independent records.

They represent how demand changes over time.

```text
Demand
  ^
125|                         *
120|                         |
115|             *
110|       *
105|
100| *
   +--------------------------------> Time
      Jan 1  Jan 2  Jan 3  Jan 4  Jan 5
```

A forecasting system can analyze these historical values and try to predict future demand.

For example:

```text
Historical Data                 Future
----------------------------------------
100 → 110 → 115 → 108 → 120 →   ???
                                  |
                                  v
                              Forecast
                                 125
```

---

# 2. Normal Data vs Time Series Data

Consider a normal customer dataset:

```text
Customer    Age    City
--------    ---    ---------
A           25     Chennai
B           30     Bengaluru
C           28     Mumbai
```

The order of rows usually does not matter.

You could rearrange the rows:

```text
Customer    Age    City
--------    ---    ---------
C           28     Mumbai
A           25     Chennai
B           30     Bengaluru
```

The meaning remains the same.

But consider:

```text
Date        Sales
----------  -----
Jan 1       100
Jan 2       120
Jan 3       140
```

If we rearrange it:

```text
Date        Sales
----------  -----
Jan 3       140
Jan 1       100
Jan 2       120
```

we lose the natural sequence.

Time-series models depend heavily on this chronological order.

---

# 3. Common Examples of Time Series Data

Time-series data exists in almost every industry.

## Retail

```text
Date        Product Sales
----------  -------------
Monday          100
Tuesday         110
Wednesday       120
Thursday        115
Friday          150
```

Used for:

* Demand forecasting
* Inventory planning
* Store staffing
* Promotion planning

---

## Banking

```text
Time        Transaction Count
----------  -----------------
09:00              200
10:00              350
11:00              420
12:00              500
```

Used for:

* Transaction volume forecasting
* Fraud pattern detection
* Server capacity planning

---

## Stock Market

```text
Date        Stock Price
----------  -----------
Monday         120
Tuesday        123
Wednesday      119
Thursday       125
Friday         128
```

---

## Weather

```text
Date        Temperature
----------  -----------
Monday        31°C
Tuesday       32°C
Wednesday     34°C
Thursday      33°C
Friday        35°C
```

---

## Server Monitoring

```text
Time        CPU Usage
----------  ---------
10:00         20%
10:05         35%
10:10         55%
10:15         80%
```

Used for:

* Detecting unusual spikes
* Infrastructure planning
* Predicting resource usage

---

## Supply Chain

```text
Week        Product Demand
----------  --------------
Week 1          1000
Week 2          1100
Week 3          1150
Week 4          1300
```

This is one of the most important applications of time-series forecasting.

---

# 4. Main Components of a Time Series

A time series can contain several patterns.

The main ones are:

```text
Time Series
    |
    +---- Trend
    |
    +---- Seasonality
    |
    +---- Cyclic Pattern
    |
    +---- Noise / Randomness
```

---

# 5. Trend

A **trend** represents the long-term direction of the data.

Example:

```text
Month       Sales
----------  -----
January      100
February     110
March        120
April        130
May          140
```

Sales are gradually increasing.

```text
Sales
 ^
 |                         *
 |                    *
 |               *
 |          *
 |     *
 +--------------------------------> Time
```

This is an **upward trend**.

Another example could be:

```text
1000 → 950 → 900 → 850 → 800
```

This represents a **downward trend**.

---

# 6. Seasonality

**Seasonality** means a pattern repeats after a predictable period.

For example, an ice-cream company may experience:

```text
Month       Sales
----------  -----
January      500
February     550
March        700
April        900
May         1200
June        1500
July        1600
August      1500
September   1100
October      800
November     600
December     550
```

Summer months have higher demand.

The same pattern may repeat every year.

```text
Demand
 ^
 |        /\              /\
 |       /  \            /  \
 |      /    \          /    \
 |_____/      \________/      \____
 +------------------------------------> Time

       Year 1           Year 2
```

Examples of seasonality include:

* Ice cream demand increasing every summer
* Umbrella demand increasing during rainy seasons
* Restaurant orders increasing every weekend
* Online shopping increasing during festivals
* Electricity consumption increasing every afternoon

---

# 7. Cyclic Pattern

A cyclic pattern also moves up and down, but unlike seasonality, it may not repeat at an exact interval.

For example:

```text
Economic Growth
      ↓
High Demand
      ↓
Slowdown
      ↓
Low Demand
      ↓
Recovery
      ↓
Economic Growth
```

These cycles can sometimes last several years.

---

# 8. Noise

Noise represents unpredictable random changes.

Example:

```text
Expected demand = 100

Actual:

98
103
101
95
106
99
```

These small changes may not have a meaningful pattern.

They can happen because of:

* Random customer behavior
* Weather changes
* Unexpected events
* Data errors
* Local events
* Supplier problems

In simple terms:

```text
Observed Data
      =
Trend
      +
Seasonality
      +
Other Patterns
      +
Noise
```

---

# 9. Types of Time Series Data

Time-series data can be classified in several ways.

---

# 9.1 Univariate Time Series

A **univariate time series** contains one main variable measured over time.

Example:

```text
Date        Sales
----------  -----
Jan 1       100
Jan 2       110
Jan 3       120
Jan 4       115
```

Only one value is being analyzed:

```text
Sales
```

The goal might be:

```text
Previous Sales
      ↓
Forecasting Model
      ↓
Future Sales
```

Examples:

* Daily sales
* Temperature
* CPU usage
* Stock price
* Number of website visitors

---

# 9.2 Multivariate Time Series

A **multivariate time series** contains multiple variables changing over time.

Example:

```text
Date      Sales    Price    Promotion    Temperature
--------  -------  -------  -----------  -----------
Jan 1      100      50          0             30
Jan 2      110      50          0             31
Jan 3      160      45          1             31
Jan 4      170      45          1             32
```

Here sales may depend on:

```text
                 Price
                   |
                   v
Promotion -----> Sales <----- Weather
                   ^
                   |
              Previous Sales
```

Multivariate forecasting can be useful because real-world demand rarely depends only on past demand.

---

# 10. Regular Time Series

A regular time series has observations collected at consistent intervals.

Example:

```text
10:00
10:05
10:10
10:15
10:20
```

The interval is always:

```text
5 minutes
```

Another example:

```text
Jan 1
Jan 2
Jan 3
Jan 4
Jan 5
```

This is daily data.

---

# 11. Irregular Time Series

An irregular time series does not have consistent intervals.

Example:

```text
10:00
10:03
10:17
10:21
11:05
```

Examples include:

* Customer transactions
* Machine failures
* Hospital visits
* Website clicks

A data engineer may need to convert irregular observations into regular intervals.

For example:

```text
Raw transactions

10:01
10:03
10:05
10:17
10:18
```

can be aggregated into:

```text
Time Window       Transactions
---------------   ------------
10:00 - 10:10          3
10:10 - 10:20          2
```

---

# 12. Continuous Time Series

Continuous time-series measurements can theoretically be observed continuously.

Examples:

* Temperature sensors
* Pressure sensors
* Machine vibration
* CPU monitoring
* Network traffic

For example:

```text
Sensor
   |
   v
Temperature Reading
   |
   v
Every Second
   |
   v
Time-Series Database
```

---

# 13. Discrete Time Series

Discrete time-series data contains values observed at specific intervals.

Example:

```text
Day       Orders
-------   ------
Monday      100
Tuesday     120
Wednesday   140
```

Orders are counted rather than continuously measured.

---

# 14. Stationary Time Series

A time series is called **stationary** when its statistical characteristics remain relatively stable over time.

For example:

```text
100, 103, 98, 101, 99, 102, 100, 97
```

The values remain around approximately the same level.

```text
Value
 ^
 |      *       *
 | *       *        *
 |    *       *          *
 +----------------------------> Time
```

There is no strong upward trend.

---

# 15. Non-Stationary Time Series

A non-stationary series changes significantly over time.

Example:

```text
100
120
140
160
180
200
```

```text
Value
 ^
 |                         *
 |                    *
 |               *
 |          *
 |     *
 +--------------------------------> Time
```

ARIMA models usually require us to investigate stationarity.

Techniques such as **differencing** can help convert a non-stationary series into a more stationary series.

---

# 16. What is Forecasting?

Forecasting means:

> Using historical data and patterns to estimate future values.

Example:

```text
Historical Demand

100 → 110 → 120 → 130 → 140

                |
                v

        Forecasting Model

                |
                v

Future Demand

150 → 160 → 170
```

The predicted values are called **forecasts**.

---

# 17. Forecasting vs Prediction

The two words are often used interchangeably, but forecasting normally has a strong **time component**.

Normal prediction:

```text
Customer Information
        ↓
Machine Learning Model
        ↓
Will Customer Churn?
```

Forecasting:

```text
Historical Sales
        ↓
Time-Series Model
        ↓
Sales Next Month
```

Forecasting specifically asks questions such as:

* What will happen tomorrow?
* What will happen next week?
* What will happen next month?
* What will demand look like next quarter?

---

# 18. Forecast Horizon

The **forecast horizon** tells us how far into the future we want to predict.

For example:

```text
Historical Data             Forecast Horizon
------------------          -----------------
Jan Feb Mar Apr May         Jun Jul Aug
```

A forecast horizon can be:

```text
1 day
7 days
30 days
3 months
1 year
```

The further we forecast into the future, the greater the uncertainty usually becomes.

```text
Today

 |
 v

Tomorrow        -> High confidence
Next Week       -> Moderate confidence
Next Month      -> Lower confidence
Next Year       -> Much more uncertainty
```

---

# 19. Why Do We Need Forecasting?

Businesses need forecasts because many decisions must be made **before the actual demand is known**.

For example, consider a supermarket.

The supermarket needs to decide today:

```text
How many products should we order for next week?
```

But next week's customer demand has not happened yet.

So:

```text
Historical Sales
       +
Seasonality
       +
Promotions
       +
Holiday Information
       ↓
Forecasting Model
       ↓
Expected Demand
       ↓
Inventory Decision
```

---

# 20. Supply Chain Demand Forecasting Example

Suppose a company sells bottled juice.

Historical weekly demand:

```text
Week        Demand
----------  ------
Week 1       1000
Week 2       1050
Week 3       1100
Week 4       1150
Week 5       1200
```

The company wants to know demand for Week 6.

A forecasting system may predict:

```text
Week 6 Demand = 1250 units
```

The supply-chain team can then plan:

```text
Forecast
   ↓
Procurement
   ↓
Production
   ↓
Warehouse Inventory
   ↓
Transportation
   ↓
Stores
   ↓
Customers
```

---

# 21. What Happens Without Demand Forecasting?

Imagine actual customer demand is:

```text
10,000 units
```

but the company stocks only:

```text
6,000 units
```

Result:

```text
High Demand
    ↓
Insufficient Inventory
    ↓
Stock-out
    ↓
Lost Sales
    ↓
Unhappy Customers
```

---

Suppose the company instead stocks:

```text
20,000 units
```

but demand is only:

```text
10,000 units
```

Result:

```text
Excess Inventory
      ↓
Storage Cost
      ↓
Unsold Products
      ↓
Possible Expiry
      ↓
Financial Loss
```

Forecasting tries to find a better balance.

```text
Too Little Inventory

          \

           Accurate Forecast

          /

Too Much Inventory
```

---

# 22. Purpose of Forecasting in Supply Chain

Forecasting helps businesses answer questions such as:

### How much should we produce?

```text
Forecasted Demand = 50,000 units

Production Planning
        ↓
Approximately 50,000 units
```

---

### How much inventory should we maintain?

```text
Demand Forecast
      +
Safety Stock
      ↓
Inventory Requirement
```

---

### How many raw materials should we purchase?

```text
Demand Forecast
        ↓
Production Requirement
        ↓
Raw Material Requirement
        ↓
Supplier Orders
```

---

### How many delivery vehicles are needed?

```text
Expected Orders
      ↓
Expected Shipment Volume
      ↓
Transportation Planning
```

---

### How much warehouse capacity is required?

```text
Expected Inventory
       ↓
Warehouse Capacity Planning
```

---

# 23. Who Uses Forecasting?

Forecasting systems can support many teams.

```text
                    Forecast
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
 Procurement      Production       Inventory
       |
       +---------------+---------------+
                       |
                       v
                 Transportation
                       |
                       v
                     Sales
```

Users may include:

* Supply-chain managers
* Inventory planners
* Procurement teams
* Manufacturing planners
* Sales teams
* Finance teams
* Warehouse managers
* Data scientists
* Data analysts
* Data engineers

---

# 24. What is the Role of a Data Engineer?

A common misconception is:

> The data engineer's job is to create the forecasting algorithm.

Usually that is **not the primary responsibility**.

A forecasting solution generally involves several roles.

```text
Data Sources
     ↓
Data Engineer
     ↓
Clean / Reliable Data
     ↓
Data Scientist / ML Engineer
     ↓
Forecasting Model
     ↓
Business Applications
```

The data engineer mainly makes sure that high-quality data reaches the forecasting system.

---

# 25. Data Engineer Responsibilities in Forecasting

A data engineer may be responsible for the following.

## 25.1 Collect Data

Data might come from:

```text
Sales Database
ERP System
Warehouse System
Supplier System
Website
Weather API
Promotion System
POS System
```

The data engineer brings these sources together.

```text
Sales DB --------\
ERP --------------\
Weather API --------> Data Pipeline
Promotion System ---/
Inventory DB -------/
```

---

# 26. Clean the Data

Real-world time-series data can contain:

* Missing dates
* Duplicate records
* Incorrect timestamps
* Null values
* Invalid quantities
* Different time zones
* Outliers

Example raw data:

```text
Date        Sales
----------  -----
Jan 1       100
Jan 2       NULL
Jan 2       110
Jan 4       -500
```

The data engineer must identify and resolve these problems.

---

# 27. Handle Missing Time Periods

Suppose the database contains:

```text
Jan 1     100
Jan 2     120
Jan 4     140
```

Jan 3 is missing.

A forecasting model may expect:

```text
Jan 1
Jan 2
Jan 3
Jan 4
```

A data engineer may create a complete calendar.

```text
Calendar Table
     +
Sales Data
     ↓
Complete Time Series
```

Result:

```text
Jan 1     100
Jan 2     120
Jan 3     Missing
Jan 4     140
```

The missing value can then be handled according to business rules.

---

# 28. Aggregate Data

Raw transactions may look like:

```text
Timestamp             Quantity
-------------------   --------
2026-01-01 09:10          2
2026-01-01 10:25          1
2026-01-01 11:40          5
```

The forecasting model may need daily demand.

The data engineer transforms this into:

```text
Date          Daily Demand
-----------   ------------
2026-01-01         8
```

Process:

```text
Individual Transactions
          ↓
Group By Date
          ↓
Daily Demand
```

---

# 29. Create Useful Time Features

Data engineers may create basic features that help forecasting.

Example:

```text
date
year
month
week
day_of_week
is_weekend
is_holiday
```

For example:

```text
Date        Demand  Day       Weekend
----------  ------  --------  -------
Jan 5        100    Monday       0
Jan 6        105    Tuesday      0
Jan 10       180    Saturday     1
```

---

# 30. Create Lag Features

A lag feature contains a previous value.

Suppose:

```text
Date        Demand
----------  ------
Jan 1       100
Jan 2       110
Jan 3       120
```

We can create:

```text
Date        Demand    Lag_1
----------  ------    -----
Jan 1       100       -
Jan 2       110       100
Jan 3       120       110
```

`Lag_1` means:

```text
Demand from one previous period
```

Other features could include:

```text
lag_1
lag_7
lag_30
```

For daily demand:

```text
lag_1  = yesterday's demand

lag_7  = demand from the same day last week

lag_30 = demand approximately one month ago
```

---

# 31. Rolling Features

A rolling feature summarizes recent historical values.

Suppose:

```text
Previous 3 days:

100
110
120
```

The three-day rolling average is:

```text
(100 + 110 + 120) / 3

= 110
```

A dataset might therefore contain:

```text
Date      Demand    Rolling_Avg_3
--------  --------  -------------
Jan 1       100          -
Jan 2       110          -
Jan 3       120        110
```

Common rolling features include:

```text
rolling_mean_7
rolling_max_7
rolling_min_7
rolling_std_7
```

---

# 32. External Features

Demand can depend on factors other than historical sales.

For example:

```text
                    Demand
                      ^
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
     Price        Promotion       Holiday
       |
       +--------------+--------------+
                      |
                      v
                   Weather
```

A useful dataset might contain:

```text
Date
Demand
Price
Promotion
Holiday
Temperature
Store
Product
```

---

# 33. Prevent Data Leakage

This is extremely important in time-series engineering.

Suppose we are forecasting January 10.

We must not use information from:

```text
January 11
January 12
January 13
```

because those values would not have been available on January 10.

Correct:

```text
Past Data
   ↓
Model
   ↓
Future Prediction
```

Wrong:

```text
Past + Future Data
       ↓
Model
       ↓
Artificially Good Prediction
```

Using future information is called **data leakage**.

---

# 34. Data Engineer vs Data Scientist

A simplified comparison is:

| Data Engineer            | Data Scientist / ML Engineer |
| ------------------------ | ---------------------------- |
| Collect data             | Explore forecasting models   |
| Build pipelines          | Train forecasting models     |
| Clean data               | Tune model parameters        |
| Aggregate time series    | Compare models               |
| Create reliable datasets | Evaluate forecasts           |
| Handle missing data      | Build ARIMA/SARIMA           |
| Create lag features      | Build LSTM                   |
| Maintain data quality    | Analyze model errors         |
| Deliver production data  | Generate predictions         |

There can be overlap depending on the organization.

---

# 35. Complete Forecasting Architecture

A supply-chain forecasting architecture might look like this:

```text
                DATA SOURCES
                     |
     +---------------+---------------+
     |               |               |
     v               v               v
 Sales DB        Inventory DB    Promotion Data
     |               |               |
     +---------------+---------------+
                     |
                     v
              Data Engineering
                     |
             ETL / ELT Pipeline
                     |
                     v
              Clean Time Series
                     |
                     v
             Feature Engineering
                     |
                     v
             Forecasting Dataset
                     |
                     v
              Forecasting Models
             /        |        \
            /         |         \
         ARIMA      SARIMA      LSTM
            \         |         /
             \        |        /
              Model Comparison
                     |
                     v
                  Forecast
                     |
                     v
            Business Decisions
                     |
        +------------+------------+
        |            |            |
        v            v            v
    Inventory    Production   Procurement
```

---

# 36. Example: End-to-End Demand Forecasting

Imagine a supermarket wants to forecast daily milk demand.

## Step 1: Historical Data

```text
Date        Milk Sold
----------  ---------
Jan 1          100
Jan 2          105
Jan 3          110
Jan 4          108
Jan 5          120
```

---

## Step 2: Add Important Information

```text
Date      Demand  Weekend  Promotion  Temperature
--------  ------  -------  ---------  -----------
Jan 1      100       0         0          30
Jan 2      105       0         0          31
Jan 3      110       0         1          31
Jan 4      108       1         0          32
Jan 5      120       1         1          32
```

---

## Step 3: Create Historical Features

```text
Date    Demand   Lag_1   Lag_7   RollingAvg_7
------  -------  ------  ------  ------------
Jan 8    125      120     100        111
```

---

## Step 4: Train Models

Possible models:

```text
Naive Forecast
Moving Average
Holt-Winters
ARIMA
SARIMA
LSTM
```

---

## Step 5: Compare Models

Example:

```text
Model            MAE
---------------  ----
Naive            18
Moving Average   15
ARIMA            12
SARIMA            9
LSTM             11
```

In this example, SARIMA performs best.

---

## Step 6: Forecast

```text
Tomorrow's predicted milk demand

= 132 units
```

---

## Step 7: Business Action

The inventory team may decide:

```text
Forecast Demand
      132
       +
Safety Stock
       18
       =
Order approximately
      150 units
```

This demonstrates that forecasting itself is not the final goal.

The actual goal is:

> **Make better business decisions using estimates of future demand.**

---

# 37. Why Data Quality Matters

Forecasting models cannot fix fundamentally incorrect input data.

Consider:

```text
Actual Demand

100
110
120
130
```

But because of pipeline errors:

```text
Stored Data

100
110
12
130
```

A forecasting model may interpret `12` as a genuine demand collapse.

Therefore:

```text
Poor Data
    ↓
Poor Model Input
    ↓
Poor Forecast
    ↓
Poor Business Decision
```

This is why data engineering is extremely important in forecasting systems.

---

# 38. Time-Series Data Pipeline

A typical pipeline is:

```text
Raw Data
   ↓
Validation
   ↓
Cleaning
   ↓
Timestamp Standardization
   ↓
Aggregation
   ↓
Missing-Period Handling
   ↓
Feature Engineering
   ↓
Forecast Dataset
   ↓
Model Training
   ↓
Forecast
```

---

# 39. Batch Forecasting Example

Many supply-chain forecasts do not need to run every second.

For example:

```text
Every Night at 1 AM
        ↓
Collect Yesterday's Sales
        ↓
Update Forecast Dataset
        ↓
Generate Next 30-Day Forecast
        ↓
Save Forecast
        ↓
Dashboard / Inventory System
```

This can be implemented as a batch data pipeline.

---

# 40. Example Forecast Table

The output could look like:

```text
Date        Product    Forecast   Lower   Upper
----------  ---------  ---------  ------  -----
Sep 10      Product A     120       110     132
Sep 11      Product A     125       112     139
Sep 12      Product A     130       115     145
```

Here:

```text
Forecast = expected demand

Lower = lower expected range

Upper = upper expected range
```

Instead of saying:

```text
Demand tomorrow WILL be 120
```

we might say:

```text
Expected demand ≈ 120

Likely range = 110 to 132
```

This represents **forecast uncertainty**.

---

# 41. Why Forecasts Are Never Perfect

Forecasts are estimates.

Unexpected events can occur.

Examples:

* Sudden festival demand
* Competitor discount
* Extreme weather
* Supply disruption
* Viral social-media trend
* Economic changes
* Product recall

Therefore:

```text
Forecast ≠ Guaranteed Future
```

Instead:

```text
Forecast = Best estimate using available historical information
```

---

# 42. Important Terms to Remember

| Term                | Meaning                                        |
| ------------------- | ---------------------------------------------- |
| Time Series         | Data collected in chronological order          |
| Timestamp           | Time associated with an observation            |
| Frequency           | How often observations occur                   |
| Trend               | Long-term direction                            |
| Seasonality         | Pattern repeating at regular intervals         |
| Cycle               | Longer irregular repeating movement            |
| Noise               | Random variation                               |
| Lag                 | Previous value of a variable                   |
| Rolling Window      | Statistics calculated over recent observations |
| Forecast            | Estimate of a future value                     |
| Forecast Horizon    | How far into the future we predict             |
| Univariate          | One primary time-varying variable              |
| Multivariate        | Multiple variables changing over time          |
| Stationarity        | Statistical behavior remains relatively stable |
| Data Leakage        | Accidentally using future information          |
| Prediction Interval | Likely range containing the future value       |

---

# 43. Simple Mental Model

Whenever you see a forecasting problem, think about:

```text
1. WHAT?

What are we forecasting?

Example:
Product demand


2. WHEN?

At what frequency?

Hourly?
Daily?
Weekly?
Monthly?


3. HOW FAR?

What is the forecast horizon?

Tomorrow?
Next 7 days?
Next 30 days?


4. WHAT HISTORY?

What previous data is available?


5. WHAT FACTORS?

Price?
Promotion?
Holiday?
Weather?


6. HOW DO WE MEASURE SUCCESS?

MAE?
RMSE?
MAPE?


7. WHAT BUSINESS DECISION?

Inventory?
Production?
Procurement?
Staffing?
```

---

# 44. Final Big Picture

```text
                     Historical Data
                           |
                           v
                    Time-Series Data
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
        Trend         Seasonality         Noise
          |                |                |
          +----------------+----------------+
                           |
                           v
                    Data Engineering
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
         Cleaning       Aggregation     Features
            |              |              |
            +--------------+--------------+
                           |
                           v
                    Forecast Dataset
                           |
                           v
                    Forecasting Model
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
        ARIMA           SARIMA            LSTM
          |                |                |
          +----------------+----------------+
                           |
                           v
                         Forecast
                           |
                           v
                    Business Decision
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      Inventory        Production       Procurement
```

---

# 45. Key Takeaway

A **time series** is data where observations occur over time and chronological order matters.

Forecasting uses historical time-series patterns to estimate future values.

For supply-chain systems:

```text
Past Demand
     ↓
Understand Patterns
     ↓
Forecast Future Demand
     ↓
Plan Inventory
     ↓
Plan Production
     ↓
Plan Procurement
     ↓
Reduce Cost + Avoid Stock-outs
```

The data engineer's key responsibility is to ensure:

```text
Correct Data
     +
Complete Data
     +
Consistent Time Intervals
     +
Useful Historical Features
     +
No Future Data Leakage
             ↓
      Reliable Forecast Dataset
```

A sophisticated forecasting model with poor data will usually produce poor forecasts.

Therefore, in a real forecasting system:

> **Reliable data engineering is the foundation on which accurate forecasting is built.**

# Common Patterns Seen in Time Series Data

When we plot time-series data with:

```text
Y-axis → Demand / Sales / Value
X-axis → Time
```

the data can show different kinds of patterns.

A forecasting engineer should first **look at the shape of the data** before deciding which forecasting technique to use.

The common patterns are:

```text
Time-Series Patterns
        |
        +---- Pure Random Pattern
        |
        +---- Linear Trend
        |
        +---- Curvilinear Trend
        |
        +---- Seasonal Pattern
        |
        +---- Seasonal Pattern + Trend
```

---

# 1. Purely Random Pattern

A purely random time series has **no clearly recognizable pattern**.

Example:

```text
Demand
 ^
 |
 |       *             *
 |  *          *                 *
 |        *          *
 |                    *
 | *                           *
 |
 +------------------------------------> Time
```

The values move randomly above and below approximately the same level.

Example data:

```text
Day       Demand
--------  ------
Day 1      102
Day 2       94
Day 3      108
Day 4       97
Day 5      105
Day 6       91
Day 7      110
Day 8       96
```

There is no obvious:

* Upward trend
* Downward trend
* Seasonal repetition
* Cyclic movement

We can think of it as:

```text
Average Demand
----------------------------

       *       *
   *                 *
          *
 *              *
                    *
```

The observations fluctuate around some average value.

---

## Real-World Example

Suppose a small shop sells a rarely purchased spare part.

Daily demand might be:

```text
0, 2, 0, 1, 4, 0, 1, 0, 3, 0
```

There may not be enough structure to identify a useful repeating pattern.

---

## Forecasting Challenge

Forecasting purely random data is difficult because:

```text
Past Pattern
     ↓
No Strong Pattern
     ↓
Little Information
     ↓
Future is difficult to predict
```

A complex model does not automatically solve this problem.

Sometimes a simple average may perform as well as a sophisticated model.

---

# 2. Increasing Linear Trend

A **linear trend** occurs when the data increases or decreases at approximately a constant rate.

Example:

```text
Demand
 ^
 |                         *
 |                     *
 |                 *
 |             *
 |         *
 |     *
 +------------------------------------> Time
```

We can draw a straight trend line through the observations:

```text
Demand
 ^
 |                        * /
 |                    *  /
 |                *   /
 |            *     /
 |        *       /
 |    *         /
 +------------------------------------> Time
```

---

## Example Data

```text
Month      Demand
---------  ------
January      100
February     110
March        120
April        130
May          140
June         150
```

Demand increases by approximately:

```text
10 units every month
```

Therefore:

```text
Month 1 → 100
Month 2 → 110
Month 3 → 120
Month 4 → 130
Month 5 → 140
```

---

## Simple Mathematical Idea

A linear trend can be represented approximately as:

```text
Y = a + bt
```

Where:

```text
Y = value we are interested in

a = starting value

b = amount of increase/decrease per time period

t = time
```

Example:

```text
Demand = 100 + (10 × Month)
```

The important idea is not the formula itself.

The important idea is:

> The series is moving approximately upward or downward at a constant rate.

---

## Real-World Example

Imagine a new food-delivery service acquiring approximately 1,000 additional orders every month.

```text
Month       Orders
----------  ------
Jan         10,000
Feb         11,000
Mar         12,000
Apr         13,000
May         14,000
```

This resembles an increasing linear trend.

---

# 3. Decreasing Linear Trend

Linear trends do not always increase.

They can also decrease.

Example:

```text
Demand
 ^
 | *
 |    *
 |       *
 |          *
 |             *
 |                 *
 +------------------------------------> Time
```

Example:

```text
Month      Demand
---------  ------
January      500
February     470
March        440
April        410
May          380
```

The product may be gradually losing popularity.

---

# 4. Curvilinear Trend

Sometimes a time series does not grow in a straight line.

Instead, the growth itself changes over time.

This creates a **curved trend**.

Example:

```text
Demand
 ^
 |                              *
 |                          *
 |                      *
 |                  *
 |             *
 |        *
 |   *  *
 +------------------------------------> Time
```

The curve may represent:

* Quadratic growth
* Exponential growth
* Logarithmic growth
* Saturating growth

---

# 5. Linear vs Curvilinear Trend

Compare the two.

## Linear

```text
Demand
 ^
 |                   *
 |              *
 |         *
 |    *
 +--------------------------> Time
```

The rate of increase is approximately constant.

---

## Curvilinear

```text
Demand
 ^
 |                         *
 |                    *
 |               *
 |          *
 |      *
 |   *
 | *
 +--------------------------> Time
```

Here the rate of growth itself is changing.

---

# 6. Example of Curvilinear Growth

Suppose an application becomes increasingly popular.

```text
Month      Users
---------  -----
Month 1      100
Month 2      120
Month 3      170
Month 4      260
Month 5      410
Month 6      650
```

The increase is not:

```text
+20
+20
+20
```

Instead:

```text
100 → 120     +20
120 → 170     +50
170 → 260     +90
260 → 410    +150
410 → 650    +240
```

The growth is accelerating.

Therefore a straight line may not describe the data well.

---

# 7. Exponential Growth Example

A simplified exponential pattern could look like:

```text
100
120
144
173
207
249
299
```

Each value increases by approximately a percentage rather than a fixed number.

Example:

```text
Previous value
      ×
Growth Rate
      ↓
Next Value
```

This type of pattern can occur in:

* User adoption
* Viral products
* Early business growth
* Network traffic
* Some biological processes

---

# 8. Seasonal Pattern

A seasonal pattern occurs when similar behavior repeats after a **fixed period**.

Example:

```text
Demand
 ^
 |       /\          /\          /\
 |      /  \        /  \        /  \
 |     /    \      /    \      /    \
 |____/      \____/      \____/      \___
 +------------------------------------------> Time
```

The important word is:

> **Repeating**

---

# 9. Weekly Seasonal Example

Consider restaurant orders:

```text
Day          Orders
-----------  ------
Monday         100
Tuesday        110
Wednesday      120
Thursday       140
Friday         180
Saturday       250
Sunday         230
```

The following week may show something similar:

```text
Monday         105
Tuesday        115
Wednesday      125
Thursday       145
Friday         190
Saturday       260
Sunday         240
```

Pattern:

```text
Mon → Low
Tue → Low
Wed → Moderate
Thu → Moderate
Fri → High
Sat → Very High
Sun → High

          ↓

Repeats every week
```

Therefore:

```text
Seasonal Period = 7 days
```

---

# 10. Other Seasonal Examples

## Hourly Seasonality

Electricity usage:

```text
Morning    → Moderate
Afternoon  → High
Night      → Low
```

Repeats approximately every day.

---

## Weekly Seasonality

Restaurant orders:

```text
Weekdays → Moderate
Weekend  → High
```

Repeats every seven days.

---

## Monthly Seasonality

Some businesses see demand patterns around:

```text
Beginning of month
Salary dates
Month end
```

---

## Yearly Seasonality

Ice cream:

```text
Summer → High Demand
Winter → Low Demand
```

Umbrellas:

```text
Rainy Season → High Demand
Dry Season   → Low Demand
```

---

# 11. Seasonal Pattern Without Trend

Consider:

```text
Year 1

100 → 150 → 200 → 150 → 100

Year 2

102 → 148 → 203 → 151 → 99

Year 3

101 → 152 → 198 → 149 → 103
```

The pattern repeats but the overall level stays approximately the same.

Diagram:

```text
Demand
 ^
 |       /\          /\          /\
 |      /  \        /  \        /  \
 |_____/    \______/    \______/    \____
 +------------------------------------------> Time
```

This is mainly **seasonality**.

---

# 12. Seasonal Pattern Plus Linear Growth

Real-world data often contains **more than one pattern at the same time**.

For example:

```text
Trend
   +
Seasonality
   =
Seasonal Pattern with Growth
```

Diagram:

```text
Demand
 ^
 |                              /\ 
 |                         /\  /  \
 |                    /\  /  \/
 |               /\  /  \
 |          /\  /  \
 |     /\  /  \
 |____/  \/ 
 +------------------------------------------> Time
```

Notice two things.

First:

```text
/\      /\      /\      /\

Repeating waves
```

This represents **seasonality**.

Second:

```text
Overall direction
       /
      /
     /
    /
```

This represents an **increasing trend**.

Together:

```text
Observed Demand
      =
Increasing Trend
      +
Seasonal Pattern
      +
Random Noise
```

---

# 13. Example: Seasonal Pattern Plus Growth

Imagine an e-commerce company.

Year 1:

```text
Month      Orders
---------  ------
Jan         1000
Feb         1100
Mar         1200
...
Nov         1700
Dec         2500
```

Year 2:

```text
Jan         1300
Feb         1400
Mar         1500
...
Nov         2100
Dec         3100
```

Year 3:

```text
Jan         1600
Feb         1700
...
Dec         3800
```

Two patterns exist.

### Pattern 1 — Growth

```text
Year 1 < Year 2 < Year 3
```

The business is growing.

### Pattern 2 — Seasonality

```text
December
    ↓
Large spike every year
```

Therefore:

```text
Demand
   =
Growth Trend
   +
December Seasonality
```

---

# 14. Important Observation

A time series does not have to contain only one component.

A real demand series might contain:

```text
Demand
   =
Trend
   +
Seasonality
   +
Promotion Effect
   +
Holiday Effect
   +
Weather Effect
   +
Random Noise
```

For example:

```text
                     Demand
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
      Trend         Seasonality       Noise
        |
        +---------------+---------------+
                        |
                        v
                  External Factors
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
       Holiday       Promotion      Weather
```

This is why real demand forecasting can become complex.

---

# 15. Visual Comparison of Major Patterns

## A. Random

```text
Demand
 ^
 |    *        *      *
 |       *  *             *
 | *              *
 |          *         *
 +----------------------------> Time
```

Interpretation:

```text
No obvious trend
No obvious seasonality
Mostly random variation
```

---

## B. Increasing Linear Trend

```text
Demand
 ^
 |                     *
 |                 *
 |             *
 |         *
 |     *
 | *
 +----------------------------> Time
```

Interpretation:

```text
Demand increases steadily over time.
```

---

## C. Curvilinear Trend

```text
Demand
 ^
 |                         *
 |                     *
 |                *
 |           *
 |       *
 |    *
 | *
 +----------------------------> Time
```

Interpretation:

```text
Demand is increasing,
but not at a constant rate.
```

---

## D. Seasonal Pattern

```text
Demand
 ^
 |      /\       /\       /\
 |     /  \     /  \     /  \
 |____/    \___/    \___/    \___
 +--------------------------------> Time
```

Interpretation:

```text
The same pattern repeats regularly.
```

---

## E. Seasonality + Increasing Trend

```text
Demand
 ^
 |                         /\
 |                    /\  /  \
 |               /\  /  \/
 |          /\  /  \
 |     /\  /  \
 |____/  \/
 +--------------------------------> Time
```

Interpretation:

```text
Demand is growing overall

AND

a seasonal pattern continues to repeat.
```

---

# 16. How to Identify the Pattern

When you receive a new time-series dataset, first plot it.

Then ask:

```text
1. Is there an overall direction?

   Yes
    ↓
   Trend


2. Does a pattern repeat?

   Yes
    ↓
   Seasonality


3. Is the trend straight?

   Yes
    ↓
   Linear Trend


4. Is the trend curved?

   Yes
    ↓
   Curvilinear Trend


5. Is there both growth and repetition?

   Yes
    ↓
   Trend + Seasonality


6. Is there no clear structure?

   Yes
    ↓
   Mostly Random / Noise
```

---

# 17. Simple Decision Diagram

```text
                 Plot Time-Series Data
                         |
                         v
               Is there a clear trend?
                    /          \
                  Yes           No
                   |             |
                   v             v
          Straight or Curved?   Repeating pattern?
             /        \          /       \
         Straight    Curved    Yes        No
            |          |        |          |
            v          v        v          v
         Linear    Curvilinear Seasonal   Random
          Trend       Trend      Pattern   Pattern
            |
            v
     Is seasonality also
        present?
        /      \
      Yes       No
       |         |
       v         v
Trend + Seasonal  Trend Only
```

---

# 18. Why Identifying the Pattern Matters

Different patterns may require different forecasting approaches.

For example:

| Pattern                     | Possible Starting Approach             |
| --------------------------- | -------------------------------------- |
| Random                      | Mean / Naive baseline                  |
| Stable level                | Moving Average / Exponential Smoothing |
| Linear Trend                | Holt's Trend Method                    |
| Trend + Seasonality         | Holt-Winters                           |
| Autocorrelated series       | ARIMA                                  |
| Trend + Seasonal dependence | SARIMA                                 |
| Complex nonlinear patterns  | Machine Learning / LSTM                |

This does **not** mean the model should be selected only by looking at the graph.

Model performance must still be measured on unseen data.

But visualization gives us an important first understanding of the series.

---

# 19. Supply-Chain Example

Suppose we plot weekly demand for a product.

### Product A

```text
*   *    *  *   *
  *   *       *
```

No obvious pattern.

Possible conclusion:

```text
Mostly random demand
```

---

### Product B

```text
100
110
120
130
140
150
```

Possible conclusion:

```text
Increasing linear trend
```

---

### Product C

```text
100
110
140
190
270
380
```

Possible conclusion:

```text
Curvilinear / accelerating trend
```

---

### Product D

```text
100
150
200
150
100

100
150
200
150
100
```

Possible conclusion:

```text
Seasonal pattern
```

---

### Product E

```text
100
150
200
150
120

130
180
230
180
150

160
210
260
210
180
```

Possible conclusion:

```text
Seasonality + increasing trend
```

---

# 20. Important Beginner Takeaway

When looking at a time-series plot, do not immediately think:

```text
"Which ML model should I use?"
```

First think:

```text
What is happening in the data?
```

Look for:

```text
                Time-Series Data
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
      Trend        Seasonality       Noise
        |
   +----+----+
   |         |
   v         v
Linear   Curvilinear
```

Then ask:

```text
Is demand increasing?

Is demand decreasing?

Does something repeat?

How frequently does it repeat?

Is the growth linear?

Is the growth curved?

How much random variation exists?

Are multiple patterns occurring together?
```

Understanding these patterns is one of the **first and most important steps in time-series analysis and forecasting**.
