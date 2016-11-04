import json
import sys

def export_browse(DB, brows_table_file):
    lnum = 0
    with open(brows_table_file, "w") as f:
        for SP in DB["species"]:
            for SEQ in DB["species"][SP]["sequences"]:
                f.write("%s,\"%s\",\"%s\",%s,%s,%s,%s\n" % (
                    lnum,
                    DB["species"][SP]["name"].replace(",","&#44;"),
                    DB["species"][SP]["sequences"][SEQ]["name"].replace(",","&#44;"),
                    DB["species"][SP]["dormancy_type"],
                    DB["species"][SP]["life_stage"],
                    len(DB["species"][SP]["sequences"][SEQ]["expressions"]),
                    SEQ,
                ))
                lnum += 1

if __name__ == "__main__":
    DB = json.load(open("dist/sources.json"))
    export_browse(DB, "hugo_files/brows.csv")
