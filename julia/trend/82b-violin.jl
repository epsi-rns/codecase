using CSV, DataFrames, Gadfly
import Cairo, Fontconfig

# Read data from CSV file
df = CSV.read("series.csv", DataFrame)
rename!(df, Symbol.(strip.(string.(names(df)))))

# Melt the DataFrame to long format for violin plot
df_long = stack(df, Not(:xs))

# Create a violin plot using Gadfly
violin_plot = Gadfly.plot(
  df_long,
  x=:variable,
  y=:value,
  color=:variable,
  Geom.violin,
  Guide.xlabel("Variable"),
  Guide.ylabel("Value"),
  Guide.title("Violin Plot for ys1, ys2, and ys3"),
  # Set ymin to 0 to avoid negative values on y-axis
  Coord.cartesian(ymin=0),
  # Set minimum y-axis value to 0
  Scale.y_continuous(minvalue=0),
  Theme(
    key_position=:top,
    default_color="purple", 
    background_color="white",
    panel_stroke=colorant"gray",
    minor_label_font_size=10pt, 
    major_label_font_size=12pt,
  )
)

# Save plot as PNG
draw(PNG("82b-violin.png", 800px, 400px), violin_plot)
