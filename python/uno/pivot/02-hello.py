# Local Library
from lib.helper import create_calc_instance

def write_to_cell(
      document: 'com.sun.star.frame.XModel',
      text: str) -> None:

    # Assuming you want to write to the first sheet
    sheet = document.getSheets().getByIndex(0)
    cell = sheet.getCellRangeByName("A1")
    cell.setString(text)

def main() -> None:
    document = create_calc_instance()

    if document:
      write_to_cell(document, 'Hello World')
      print("Hello World written to cell A1.")

if __name__ == "__main__":
    main()
