using CSV, DataFrames, StatsPlots

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Create scatter plot with marginal density plots
scatter_with_marginals = @df df scatter(
    :xs, :ys3,
    legend = false,
    markerstrokewidth = 0,
    markersize = 2,
    markeralpha = 0.5,
    title = "Scatter Plot with Marginal Density",
    xlabel = "xs",
    ylabel = "ys3",
    smooth = true,
    linecolor = :blue,
    lw = 0.2,
    legendtitle = "",
    label = false,
    marginalhist = :both,  # Add marginal histograms
    subplot = (2,2),       # Layout for subplot
)

# Save plot as PNG
savefig("85a-marginal.png")
