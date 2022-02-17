from datetime import datetime
import csv

from localparser import parse
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from typing import List

def format_date(date: str, filter_first=False):
    date_list = date.split(" ")
    if filter_first:
        date_list = date_list[1::]
    date_list = date_list[::-1]

    return '-'.join(date_list)

def get_data(result):
    data_list = result.text.split("\n")
    from_date = format_date(data_list[7], filter_first=True)
    to_date = format_date(data_list[8], filter_first=True)
    paid_date = format_date(data_list[13])
    cost = data_list[16].split(" ")[0]

    #The presence of an extra line in the list shifts everything one place, if that happens then simply parse the next line
    if "smc" in data_list[29]:
        cubic_meters = data_list[29].split(" ")[0]
    else:
        cubic_meters = data_list[30].split(" ")[0]


    return [paid_date, from_date, to_date, cost, cubic_meters]

def save_csv(args, values: List[str]):
    with open(args.output_file, "a") as fw:
        writer = csv.writer(fw)
        writer.writerow(values)

def main():
    args = parse()

    opts = Options()
    opts.headless = True
    assert opts.headless

    with Chrome(options=opts) as browser:
        with open(args.filename, "r") as f:
            for url in f.readlines():
                browser.get(url)
                result = browser.find_element(value="bolletta_elettronica")
                values = get_data(result)
                print(values)
                save_csv(args,values)

if __name__ == "__main__":
    main()




