"""
Simple domain extraction
@date:  27/01/2026
"""

import re

import pandas as pd


def is_valid_domain(domain: str) -> bool:
    pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))


df = pd.read_csv("test.csv")

urls = []
for index, row in df.iterrows():
    if row["Protocol"] == "DNS":
        info_details = row["Info"].split(" ")
        # print(info_details)
        for info in info_details:
            if is_valid_domain(info):
                try:
                    urls.index(info)
                except:
                    urls.append(info)

print("\n".join(urls))
with open("domains.txt", "w") as f:
    f.write("\n".join(urls))
