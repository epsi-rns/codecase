# Local Library
from lib.helper import (
  get_desktop, create_calc_instance, get_file_path)

def write_to_cell(
      document: 'com.sun.star.sheet.SpreadsheetDocument',
      text: str) -> None:

    # Assuming you want to write to the first sheet
    sheet = document.getSheets().getByIndex(0)
    cell = sheet.getCellRangeByName("A1")
    cell.setString(text)

def main() -> None:
    # Getting the source sheet
    desktop   = get_desktop()
    document  = create_calc_instance(desktop)

    if document:
      write_to_cell(document, 'Hello World')
      print("Hello World written to cell A1.")

if __name__ == "__main__":
    main()

