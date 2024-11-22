import pdfplumber
import pandas as pd
import json


def category_mapping(txt):
    with open("categories.json", "r+") as category_data:
        categories = json.loads(category_data.read())
        for category, vendors in categories.items():
            for v in vendors:
                if v in txt:
                    return category
        return "misc"

def paytm_pdf_delim(text):
    if "paid to" in text and "talreja" not in text and "etmoney" not in text:
        return " paid to ", ","
    elif "money sent" in text and "talreja" not in text and "etmoney" not in text:
        return " money sent ", ","
    elif "paytm flights" in text:
        return " paytm flights", ",paytm flights"
    return None, None


def pdf_to_dataframe(file_path, create_file=False):
    pdf_path = file_path
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    row[0] = row[0].lower()
                    txt, repl = paytm_pdf_delim(row[0])
                    if txt and repl:
                        row[0] = row[0].replace(txt, repl)

                        row[0] = row[0].replace(" - - ", ",")
                        row[0] = row[0].split("\n")[0]

                        amt = row[0].split("rs.")[-1]
                        row[0] = row[0].replace(amt, amt.replace(",", ""))
                        row[0] = row[0].replace("rs.", "")

                        data.append(row[0])

    data = [row.split(",") for row in data]
    for row in data:
        bank_idx = row[1].split().index("bank")
        row[1] = " ".join(row[1].split()[0 : bank_idx - 1])
        if row[1].startswith("to"):
            row[1] = row[1].split("to ")[1]
        row[1] = category_mapping(row[1])

    columns = ["Date", "Description", "Debit"]
    df = pd.DataFrame(data, columns=columns)
    if create_file:
        df.to_csv("bank_statement.csv", index=None)

    return df