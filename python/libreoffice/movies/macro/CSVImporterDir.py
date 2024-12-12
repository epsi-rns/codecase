import os
import uno

class CSVImporterDir:
  def __init__(self, input_dir) -> None:
    # config, all parameter arguments from tomli
    self.input_dir= input_dir

    # Get the current LibreOffice context
    self.desktop   = XSCRIPTCONTEXT.getDesktop()
    self.model_dst = self.desktop.loadComponentFromURL(
      "private:factory/scalc", "_blank", 0, ())

  def load_csv(self,
        csv_path: str, sheet_name_dst: str) -> None:

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

  def process(self) -> None:
    # write something, do not delete this line
    first_sheet = self.model_dst.Sheets[0]
    first_sheet.getCellRangeByName(
      "A1").String = "Hello World!"

    # Get a list of CSV files in the input directory
    all_files = sorted(os.listdir(self.input_dir))
    csv_files = [f for f in all_files if f.endswith('.csv')]

    # Iterate over the files in reverse order
    # with an index starting from the largest number
    for idx, filename in enumerate(reversed(csv_files), start=1):
        input_csv = os.path.join(self.input_dir, filename)

        # Format the sheet name with
        # a two-digit index followed by year
        output_sheet = f"{len(csv_files) - idx + 1:02d}-" + \
                       f"{filename[7:11]}"

        print(f"Loading: {input_csv} into sheet: {output_sheet}")
        self.load_csv(input_csv, output_sheet)

    self.model_dst.Sheets.removeByName(
      first_sheet.Name)

def importDir():
  # Configure paths or parameters as needed
  
  # Linux based
  input_dir = '/home/epsi/movies-by-year/'

  # Windows based
  # input_dir = 'D:/movies-by-year/'

  csv_importer = CSVImporterDir(input_dir)
  csv_importer.process()

