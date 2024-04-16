using CSV, DataFrames, StatsPlots

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Extract the columns ys1, ys2, and ys3
data = [df.ys1, df.ys2, df.ys3]

# Create a violin plot using StatsPlots
violin(data, 
  labels = ["ys1", "ys2", "ys3"],
  linecolor = :black,
  legend = false,
  xlabel = "Variable",
  ylabel = "Value",
  title = "Violin Plot for ys1, ys2, and ys3",
  grid = false)

# Save plot as PNG
savefig("81b-violin.png")
