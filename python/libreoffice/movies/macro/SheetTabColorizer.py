# Google Material color scale 
blueScale = {
  0: 0xE3F2FD, 1: 0xBBDEFB, 2: 0x90CAF9,
  3: 0x64B5F6, 4: 0x42A5F5, 5: 0x2196F3,
  6: 0x1E88E5, 7: 0x1976D2, 8: 0x1565C0,
  9: 0x0D47A1
}

tealScale = {
  0: 0xE0F2F1, 1: 0xB2DFDB, 2: 0x80CBC4,
  3: 0x4DB6AC, 4: 0x26A69A, 5: 0x009688,
  6: 0x00897B, 7: 0x00796B, 8: 0x00695C,
  9: 0x004D40
}

amberScale = {
  0: 0xFFF8E1, 1: 0xFFECB3, 2: 0xFFE082,
  3: 0xFFD54F, 4: 0xFFCA28, 5: 0xFFC107,
  6: 0xFFB300, 7: 0xFFA000, 8: 0xFF8F00,
  9: 0xFF6F00
}

brownScale = {
  0: 0xEFEBE9, 1: 0xD7CCC8, 2: 0xBCAAA4,
  3: 0xA1887F, 4: 0x8D6E63, 5: 0x795548,
  6: 0x6D4C41, 7: 0x5D4037, 8: 0x4E342E,
  9: 0x3E2723
}

class SheetTabColorizer:
  def __init__(self):
    # Get the current LibreOffice context and document
    self.desktop  = XSCRIPTCONTEXT.getDesktop()
    self.document = XSCRIPTCONTEXT.getDocument()

    # List of palettes to cycle through
    self.palettes = [blueScale, tealScale, amberScale, brownScale]

  def apply_color_to_sheets(self):
    # Loop through each sheet and apply color based on index
    sheets = self.document.Sheets

    for i in range(sheets.Count):
      sheet = sheets[i]
      
      # Determine which palette to use based on sheet index
      palette_index = (i // 10) % 4  # Cycle through 4 palettes
      color_index = i % 10  # Cycle through 0 to 9 for each palette

      # Get the color from the selected palette
      tab_color = self.palettes[palette_index][color_index]
      sheet.TabColor = tab_color  # Set the tab color

  def run(self):
    # Run the colorizing function
    self.apply_color_to_sheets()

def main():
  # Create the colorizer instance and run it
  colorizer = SheetTabColorizer()
  colorizer.run()

# Program entry point
if __name__ == "__main__":
  main()
