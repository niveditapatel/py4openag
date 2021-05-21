# PY4OPENAG

This open-source package aims to establish the ML4Ops pipeline from public databases to integrated analytics for agriculture. It provides  a variety of functions  to study climate trends and simplify the calculation of commonly used metrics in agriculture, such as growing degree days, extreme heat degree days, the base temperature for different crop types, as well as basic climate metrics like average temperature and total precipitation for user specified time periods. The package also includes unsupervised and supervised learning based on these metrics. . 

The development of this package is supported by the SMARTFARM project. The SMARTFARM program of DOE’s Advanced Research Projects Agency-Energy (ARPA-E) aims to innovate technologies that can help to cost-effectively and efficiently quantify feedstock emissions at the field level. The project aspires to facilitate advanced biofuels that can potentially be a carbon-negative source of energy and aims to promote environmental sustainability while simultaneously increasing farmer profitability and productivity. 


## Functions In The Package:

#### Annual Average Temperature: average_temperature
 
This function calculates the average temperature based on the time series (daily) and the time frame specified by input year and months.    
 
Input: \
Temperature time series - daily: pandas data frame \
Time series data frame that contains dates and daily temperature values. \
Year: integer \
This value specifies the year for which calculation average temperature has to be calculated. \
Months: array (int), Default=[1,12]\
Two-dimensional array specifies the starting month and ending month for which average temperature has to be calculated.
 
Output:\
Avg: float:\
Returns average temperature value
 
 
#### Annual Total Precipitation: total_precipitation
 
This function calculates the total precipitation based on the time series (daily) and the time frame specified by input year and months.    
 
Input: \
Temperature time series - daily: pandas data frame \
Time series data frame that contains dates and daily precipitation values. \
Year: integer\
This value specifies the year for which calculation average temperature has to be calculated. \
Months: array (int), Default=[1,12]\
Two-dimensional array specifies the starting month and ending month for which average temperature has to be calculated.
 
Output:\
sum: float:\
Returns sum of precipitation value
 
 
#### Extreme Degree Days: extreme_degree_days
 
This function calculates the value of extreme degree days based on the time series (daily) and the time frame specified by input year and months.    
 
Input: \
Temperature time series - daily: pandas data frame \
Time series data frame that contains dates and daily temperature values. <br> 
Threshold Temperature: float \
This value specifies the temperature value above which days are considered in the extreme degree days sum.\
Year: integer\
This value specifies the year for which calculation average temperature has to be calculated. \
Months: array (int), Default=[1,12]\
Two-dimensional array specifies the starting month and ending month for which average temperature has to be calculated.
 
Output:\
extreme_degree_days: float \
Returns value of extreme degree days
 
#### Growing degree days: growing_degree_days
 
This function computes the growing degree days based on the temperature time series (daily) and the base temperature. The base temperature depends on the crop and can be found using the growingdays_basetemp() function.
 
Input: \
Temperature time series - daily: pandas data frame \
Time series data frame that contains dates and daily temperature values. \
Year: integer \
This value specifies the year for which calculation average temperature has to be calculated. \
Base temperature: float:\
This value specifies the base temperature \
Output: \
Growing degree days: float\
Returns value of growing degree days
 
#### Base Temperature For Growing Degree Days: growingdays_basetemp 
 
This function provides the base temperature for a certain crop. The data is based on the baselines provided from reference [Reference Link](https://en.wikipedia.org/wiki/Growing_degree-day).
 
Input: \
Crop type: string \
String value specifies the crop type that bast temperature needs to be determined for. Enter value from: [wheat,barley,rye,oats,flaxseed,lettuce,asparagus,sunflower,potato,maize,sorghum,rice,soybeans,tomato,coffee] 
 
Output: \
Base temperature: float \
Returns the base temperature value in degrees celsius
 
#### Temperature Trend: temptrend
 
This function calculates a series of annual average temperature for the years specified and linear regression of annual average temperature as a function of year. 
 
Input: \
Temperature time series - daily: pandas data frame \
Time series data frame that contains dates and daily temperature values. \
Years: array (int)\
Two dimensional array specifies the starting year and ending year for which trend has to be determined. Years should be entered as integers in the array.
 
Output:\
R-value: float\
Pearson correlation coefficient for year vs annual T time series\
P-value: float\
P-value of trend\
Regression coefficient: float\
Slope/trend of year vs annual temperature

## Demonstration Of Functions:

1. [Download data from GEE](https://colab.research.google.com/drive/1hjUK8Dm66VqoQkbXcvv-405CT4wGDuPL)
2. [Running functions](https://colab.research.google.com/drive/12RtHj3OmjxfOxZadWmA93v9vXr8bYqV6)

