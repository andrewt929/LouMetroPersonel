# PROJECT SETUP - Importing packages
import pandas as pd


# SOURCE DATA
## Code for loading from online repository
csv_url = 'https://data.louisvilleky.gov/sites/default/files/SalaryData_99.csv'
## Code for loading a downloaded csv
#from pathlib import Path
#csv_url = Path("C:/Users/ataylor/Documents/Personal/LousivilleMetroSalaryAnalysis/SalaryData_99.csv")

data = pd.read_csv(csv_url)


## EXPLORE THE DATA
#print("The initial shape is: ", data.shape)
#print("The column names and data types are: ", data.dtypes)


# CLEAN THE DATA
## Remove Duplicates
### SQL Equivalent: SELECT DISCTINCT * FROM data
data = data.drop_duplicates()

## Select & Treat Blanks - Drop rows with blanks
### SQL Equivalent: SELECT DISTINCT * FROM data WHERE * <> ''
data = data.dropna()

# Filter out latest year to make total compensation easier
### SQL Equivalent: SELECT DISTINCT * FROM data WHERE CalendarYear <> max(CalendarYear)
data = data[data["CalendarYear"] != max(data.CalendarYear)]

#print("The cleaned shape is: ", data.shape)


# CREATE GROUPINGS
latestYear = data.groupby(['EmployeeName', 'Department'])['CalendarYear'].max().reset_index()
earliestYear = data.groupby(['EmployeeName', 'Department'])['CalendarYear'].min().reset_index()

careers = latestYear.merge(earliestYear, how = 'left', left_on = ['EmployeeName', 'Department'], right_on = ['EmployeeName', 'Department'], suffixes = ('Latest', 'Earliest'))
salaries = careers.merge(data[["EmployeeName", "Department", "CalendarYear", "YearToDate"]], how = 'left', left_on = ['EmployeeName', 'Department', 'CalendarYearLatest'], right_on = ['EmployeeName', 'Department', 'CalendarYear'])
salaries = salaries[salaries["YearToDate"] > 0]
salaries = salaries.merge(data[["EmployeeName", "Department", "CalendarYear", "YearToDate"]], how = 'left', left_on = ['EmployeeName', 'Department', 'CalendarYearEarliest'], right_on = ['EmployeeName', 'Department', 'CalendarYear'])

## Cleanup names
salaries = salaries.rename(index = str, 
                           columns = {"EmployeeName": "Employee"
                                      , "CalendarYearLatest": "LatestYear"
                                      , "CalendarYearEarliest": "EarliestYear"
                                      , "YearToDate_x": "LatestIncome"
                                      , "YearToDate_y": "EarliestIncome"})
salaries = salaries.drop(["CalendarYear_x", "CalendarYear_y"], axis = 1)

## Add calculated columns
salaries["Seniority (yrs)"] = salaries["LatestYear"] - salaries["EarliestYear"]
salaries["WageChange"] = salaries["LatestIncome"] - salaries["EarliestIncome"]
salaries["WageRate ($/yr)"] = salaries["WageChange"]/salaries["Seniority (yrs)"]
salaries = salaries[salaries["Seniority (yrs)"] > 1]
salaries = salaries[salaries["WageChange"] >= 0]


# Output CSV
salaries.to_csv('salaryData.csv')