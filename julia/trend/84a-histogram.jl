using CSV, DataFrames, StatsPlots

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Melt the DataFrame to long format for histplot
df_long = stack(df, Not(:xs))

# Create histogram plot using StatsPlots with custom colors
hist_plot = histogram(
    df_long.value,
    group = df_long.variable,
    bins = collect(0:50:maximum(df_long.value)),
    linecolor = :black,
    fillalpha = 0.7,
    color = :Set1,
    xlabel = "Value",
    ylabel = "Density",
    title = "Histogram Plot for ys1, ys2, and ys3",
    legend = :topleft
)

# Save plot as PNG
savefig("84a-histogram.png")
