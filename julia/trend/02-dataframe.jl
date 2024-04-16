using CSV, DataFrames

# Read data from CSV file
# Strip spaces from column names
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

println(last(df,5))
println()
println(names(df))

