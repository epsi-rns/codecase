# Main Program
#-------------

import tomli, csv
from datetime import datetime
from openpyxl import Workbook, load_workbook

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class CSVImporter:
    def __init__(self, config_path, output_xlsx):
        # config, all parameter arguments from tomli
        self.config_path = config_path
        self.output_xlsx = output_xlsx
        self.set_config()

        # Create a new workbook
        self.wb = Workbook()
        self.default_sheet = self.wb.active

        # Placeholder, will be deleted later
        self.default_sheet.title = "Temp"

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

    def detect_value_type(self, value):
        """Detect if value is a number, date, or text"""

        # Handle empty values
        if value.strip() == "":
            return None  

        # Try parsing as a date
        date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%b-%Y"]
        for fmt in date_formats:
            try:
                # Convert to datetime
                return datetime.strptime(value, fmt)
            except ValueError:
                # Try next format
                continue

        # Try converting to a number
        try:
            # Try to convert to int if no decimal point
            if "." not in value:
                return int(value)
            # Convert to float if it has a decimal point
            return float(value)
        except ValueError:
            # Keep as string if conversion fails
            return value

    def load_csv(self, csv_path, sheet_name_dst):
        """Load CSV into a new sheet"""
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            # Create new sheet
            ws = self.wb.create_sheet(title=sheet_name_dst)

            for row in reader:
                # Convert numbers while keeping strings unchanged
                converted_row = [self.detect_value_type(cell) for cell in row]

                # Appending rows from CSV
                ws.append(converted_row)

    def process(self):
        # Main logic for importing CSV files
        for filename in self.filenames:
            input_csv    = filename['input-expand']
            output_sheet = filename['sheet-expand']

            print(f"Loading: {input_csv} into sheet: {output_sheet}")
            self.load_csv(input_csv, output_sheet)

        # Remove the initial temporary sheet
        if "Temp" in self.wb.sheetnames:
            self.wb.remove(self.wb["Temp"])

        # Save the workbook
        self.wb.save(self.output_xlsx)

def main() -> None:
    # Configure paths or parameters as needed
    config_path = '/home/epsi/Dev/config.toml'  
    output_xlsx = 'movies_by_year.xlsx'

    csv_importer = CSVImporter(config_path, output_xlsx)
    csv_importer.process()

if __name__ == "__main__":
    main()