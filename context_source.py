import os
import json
import csv
from PyPDF2 import PdfReader

class ContextSource:
    # a path a paramétere az osztálynak
    def __init__(self, path):
        self.path = path

    def parse_to_string(self):
        _, extension = os.path.splitext(self.path)
        if extension == ".txt" or extension == ".cs" or extension == ".py" or extension == ".js":
            return self._process_txt()
        elif extension == ".csv":
            return self._process_csv()
        elif extension == ".json":
            return self._process_json()
        elif extension == ".pdf":
            return self._process_pdf()
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
    def _process_txt(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return file.read()

    def _process_csv(self):
        with open(self.path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            return "\n".join([", ".join(row) for row in reader])

    def _process_json(self):
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return json.dumps(data, indent=2)

    def _process_pdf(self):
        reader = PdfReader(self.path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text