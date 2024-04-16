using CSV, DataFrames, Gadfly
import Cairo, Fontconfig

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Melt the DataFrame to long format for boxplot
df_long = stack(df, Not(:xs))

# Create a boxplot using Gadfly
box_plot = Gadfly.plot(
  df_long,
  x=:variable,
  y=:value,
  color=:variable,
  Geom.beeswarm(),
  Guide.xlabel("Variable"),
  Guide.ylabel("Value"),
  Guide.title("Swarm Plot for ys1, ys2, and ys3"),
  Theme(
    key_position = :top,
    background_color = "white",
  )
)

# Save plot as PNG
draw(PNG("82c-swarm.png", 800px, 400px), box_plot)
