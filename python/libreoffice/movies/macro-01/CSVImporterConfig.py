import tomli
import uno

# https://help.libreoffice.org/latest/ro/text/shared/guide/csv_params.html

class CSVImporter:
  def __init__(self, config_path) -> None:
    # config, all parameter arguments from tomli
    self.config_path = config_path
    self.set_config()

    # Get the current LibreOffice context
    self.desktop   = XSCRIPTCONTEXT.getDesktop()
    self.model_dst = self.desktop.loadComponentFromURL(
      "private:factory/scalc", "_blank", 0, ())

  def set_config(self) -> None:
    # read toml configuration
    file_obj: TextIO = open(self.config_path, 'rb')
    config_root = tomli.load(file_obj)
    file_obj.close()

    # Get config content.
    path_root = config_root.get('path', '.')
    csv_s     = config_root.get('csv_s', [])

    # Define input and output file paths
    filenames = []
    for index, csv in enumerate(csv_s):
      filenames.append({
        'input-expand' : f'{path_root}/{csv}.csv',
        'sheet-expand' : f'{index+1:02d}-{csv[7:11]}', 
      })

    self.filenames = filenames

  def load_csv(self, csv_path, sheet_name_dst):
    # Prepare filter options for CSV import\
    filter_options = "44,34,0,1,"
    file_url = uno.systemPathToFileUrl(csv_path)

    # Set properties for loading the CSV file
    properties = (
        uno.createUnoStruct("com.sun.star.beans.PropertyValue"),
        uno.createUnoStruct("com.sun.star.beans.PropertyValue"),
    )
    properties[0].Name  = "FilterName"
    properties[0].Value = "Text - txt - csv (StarCalc)"
    properties[1].Name  = "FilterOptions"
    properties[1].Value = filter_options

    # Load the CSV file as a spreadsheet
    model_src = self.desktop.loadComponentFromURL(
      file_url, "_blank", 0, properties)
    model_src.Sheets[0].Name = sheet_name_dst
    self.model_dst.Sheets.importSheet(
      model_src, sheet_name_dst, 0)
    model_src.close(True)

  def process(self, sheetType) -> None:
    # write something, do not delete this line
    first_sheet = self.model_dst.Sheets[0]
    first_sheet.getCellRangeByName(
      "A1").String = "Hello World!"

    # Main function to load Pivot CSV 
    for filename in reversed(self.filenames):
      input_csv    = filename['input-expand']
      output_sheet = filename['sheet-expand']

      print(f"Loading: {input_csv}")
      self.load_csv(input_csv, output_sheet)

    self.model_dst.Sheets.removeByName(
      first_sheet.Name)

def importCSVs():
  # Configure paths or parameters as needed
  config_path = '/home/epsi/Dev/config.toml'  
  csv_importer = CSVImporter(config_path)
  csv_importer.process('Tabular')

