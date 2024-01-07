import os

# Local Library
from lib.helper import (
  get_desktop, open_document, get_file_path)

def write_to_cell(
      document: 'com.sun.star.sheet.SpreadsheetDocument',
      text: str) -> None:

    # Assuming you want to write to the first sheet
    sheet = document.getSheets().getByIndex(0)
    cell = sheet.getCellRangeByName("A1")
    cell.setString(text)

def main() -> None:
    # Get the directory where the current script is located
    # Create the file path for your test.ods file
    # Now you can use file_path to open your test.ods file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "test.ods")

    # Getting the source sheet
    desktop   = get_desktop()
    document  = open_document(desktop, file_path)

    if document:
      write_to_cell(document, 'Hello World')
      print("Hello World written to cell A1"
          + " in the specified document.")

if __name__ == "__main__":
    main()

