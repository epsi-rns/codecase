import os
import csv
from openpyxl import Workbook, load_workbook

class CSVImporterDir:
    def __init__(self, input_dir, output_xlsx):
        self.input_dir = input_dir
        self.output_xlsx = output_xlsx

        # Create a new workbook
        self.wb = Workbook()
        self.default_sheet = self.wb.active

        # Placeholder, will be deleted later
        self.default_sheet.title = "Temp"

    def load_csv(self, csv_path, sheet_name_dst):
        """Load CSV into a new sheet"""
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            # Create new sheet
            ws = self.wb.create_sheet(title=sheet_name_dst)

            for row in reader:
                # Appending rows from CSV
                ws.append(row)  

    def process(self):
        """Main logic for importing CSV files"""
        all_files = sorted(os.listdir(self.input_dir))
        csv_files = [f for f in all_files if f.endswith('.csv')]

        for idx, filename in enumerate(csv_files, start=1):
            input_csv = os.path.join(self.input_dir, filename)
            output_sheet = f"{idx:02d}-{filename[7:11]}"

            print(f"Loading: {input_csv} into sheet: {output_sheet}")
            self.load_csv(input_csv, output_sheet)

        # Remove the initial temporary sheet
        if "Temp" in self.wb.sheetnames:
            self.wb.remove(self.wb["Temp"])

        # Save the workbook
        self.wb.save(self.output_xlsx)

def main() -> None:
    input_dir = '/home/epsi/movies-by-year/'
    output_xlsx = 'movies_by_year.xlsx'

    csv_importer = CSVImporterDir(input_dir, output_xlsx)
    csv_importer.process()

if __name__ == "__main__":
    main()