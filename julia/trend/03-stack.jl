using CSV, DataFrames

# Read data from CSV file
# Strip spaces from column names
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Melt the DataFrame to long format
df_long = stack(df, Not(:xs))

show(df_long, allrows=false)
println("\n")

show(names(df_long))
