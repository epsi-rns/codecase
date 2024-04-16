using CSV, DataFrames, StatsPlots

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Melt the DataFrame to long format for histplot
df_long = stack(df, Not(:xs))

print(df_long, "\n")

# Define custom colors for each group
custom_colors = Dict(
    "ys1" => :red,
    "ys2" => :green,
    "ys3" => :blue
)

print(custom_colors, "\n")

# Create histogram plot using StatsPlots.jl with custom colors
hist_plot = histogram(
    df_long.value,
    group = unique(df_long.variable),
    bins = collect(0:50:maximum(df_long.value)),
    linecolor = :black,
    fillalpha = 0.7,
    # Use custom colors for each group
    color = [custom_colors[x] for x in df_long.variable],  
    xlabel = "Value",
    ylabel = "Density",
    title = "Histogram Plot for ys1, ys2, and ys3",
    legend = :topleft
)

# Save plot as PNG
savefig("84b-histogram.png")
