import json
import sys
import yaml

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

def export_sequence_pages(DB, pages_path):
    for SP in DB:
        for SEQ in DB["species"][SP]["sequences"]:
            with open("%s/%s.md" % (path, uniprot), "w") as f:
                md_data = {}
                md_data["title"] = uniprot
                md_data["description"] = uniprot
                md_data["date"] = "2016-07-01"
                #
                md_data["genename"] = SalmoNet["node"][uniprot]["name"]
                md_data["locus"] = SalmoNet["node"][uniprot]["locus"]
                md_data["strain"] = SalmoNet["node"][uniprot]["strain"]
                md_data["orthologs"] = SalmoNet["node"][uniprot]["orthologs"]
                md_data["uniprot"] = uniprot
                md_data["interactioncsv"] = "\n".join(SalmoNet["node"][uniprot]["interactions"])
                #
                md = yaml.dump(md_data, allow_unicode=True,
                          default_flow_style=False,
                          explicit_start=True, explicit_end=True,
                          default_style="'", line_break="/n")[:-4]
                md += "---\n"
                f.write(md)

if __name__ == "__main__":
    DB = json.load(open("dist/sources.json"))
    export_browse(DB, "hugo_files/brows.csv")
