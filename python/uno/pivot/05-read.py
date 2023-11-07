# Local Library
from lib.helper import (
  open_document, get_file_path)

class CellReader:
  def __init__(self,
      file_path: str, sheetName: str) -> None:

    # save initial parameter
    self.url = f"{file_path}"

    # Getting the source sheet
    self.document = open_document(self.url)

    if self.document:
      # Assuming the first sheet
      self.sheet = self.document. \
        Sheets[sheetName]

  def read(self) -> None:
    print(self.sheet['A1'].getString())
    print(self.sheet['B1'].getString())
    print(self.sheet['C1'].getString())

  def process(self) -> None:
    self.read()

def main() -> int:
  file_path = get_file_path('test.ods')

  sample = CellReader(file_path, 'Table')
  sample.process()
  
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
