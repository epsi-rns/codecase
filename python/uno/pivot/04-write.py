# Local Library
from lib.helper import (
  get_desktop, create_calc_instance, get_file_path)

class CellWriter:
  def __init__(self,
      file_path: str, sheetName: str) -> None:

    # save initial parameter
    self.url = f"file://{file_path}"

    # Getting the source sheet
    desktop = get_desktop()
    self.document = create_calc_instance(desktop)

    if self.document:
      # Assuming the first sheet
      self.sheet = self.document.getSheets()[0]
      self.sheet.setName(sheetName)

  def write(self) -> None:
    self.sheet['A1'].setString('Number')
    self.sheet['B1'].setString('Date')
    self.sheet['C1'].setString('Categories')

  def process(self) -> None:
    self.write()
    print('Writing Header')

    try:
      self.document.storeToURL(self.url, ())
      print('Saving File')
    except Exception as e:
      print(f"Error saving the document: {str(e)}")

def main() -> int:
  file_path = get_file_path('test.ods')

  sample = CellWriter(file_path, 'Table')
  sample.process()
  
  return 0

if __name__ == "__main__":
  raise SystemExit(main())

