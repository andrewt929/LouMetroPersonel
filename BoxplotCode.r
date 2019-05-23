# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset <- data.frame(Annual Raise ($/yr), Seniority (yrs), Department)
# dataset <- unique(dataset)

# Paste or type your script code here:

Department <- dataset$Department
WageRate <- dataset$"Annual Raise ($/yr)"

bymedian <- with(dataset, reorder(Department, WageRate, median))
op <- par(mar = c(5, 15, 2, 2) + 0.1)

boxplot(WageRate~bymedian,
data = dataset,
main = "Average Annual Wage Increase by Department",
xlab="USD",
col="blue",
border="green",
horizontal = TRUE,
las = 2,
notch = TRUE,
boxwex = 0.4,
cex.axis=0.9
)
par(op)