using CSV, DataFrames, StatsPlots

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Melt the DataFrame to long format for KDE plot
df_long = stack(df, Not(:xs))

# Create KDE plot using StatsPlots with custom colors
kde_plot = density(
  df_long.value, 
  group = df_long.variable,
  fillalpha = 0.7,
  legend = :topright,
  xlabel = "Value",
  ylabel = "Density",
  title = "KDE Plot for ys1, ys2, and ys3",
  lw = 2, # Line width
  α = 0.5 # Opacity
)

# Save plot as PNG
savefig("83a-kdeplot.png")
