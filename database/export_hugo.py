import json
import sys
import yaml
import cgi

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
    arrows = {
        'variable': "<i class=\"uk-icon-line-chart uk-icon-medium\"></i>",
        'stable': "<i class=\"uk-icon-arrows-h uk-icon-medium\"></i>",
        'up': "<i class=\"uk-icon-arrow-up uk-icon-medium\"></i>",
        'detected': "<i class=\"uk-icon-check-square-o uk-icon-medium\"></i>",
        'down': "<i class=\"uk-icon-arrow-down uk-icon-medium\"></i>",
    }
    gender = {
        'female': "<i class=\"uk-icon-venus uk-icon-medium\"></i>",
        'male': "<i class=\"uk-icon-mars uk-icon-medium\"></i>",
        '': "n.a.",
    }
    for SP in DB["species"]:
        for SEQ in DB["species"][SP]["sequences"]:
            with open("%s/%s.md" % (pages_path, SEQ), "w") as f:
                md_data = {}
                md_data["title"] = DB["species"][SP]["sequences"][SEQ]["name"]
                md_data["description"] = DB["species"][SP]["sequences"][SEQ]["name"]
                md_data["date"] = "2016-11-01"
                # add sequence specific data
                md_data["sequence_name"] = DB["species"][SP]["sequences"][SEQ]["name"]
                md_data["sequence_ncbi"] = DB["species"][SP]["sequences"][SEQ]["ncbi"]
                md_data["sequence_type"] = DB["species"][SP]["sequences"][SEQ]["type"]
                md_data["sequence_note"] = DB["species"][SP]["sequences"][SEQ]["note"]
                md_data["sequence_other_id"] = DB["species"][SP]["sequences"][SEQ]["other_id"]
                md_data["sequence_other_id_type"] = DB["species"][SP]["sequences"][SEQ]["other_id_type"]
                md_data["species_name"] = DB["species"][SP]["name"]
                md_data["species_taxid"] = SP
                md_data["species_ordo"] = DB["species"][SP]["ordo"]
                expressioncsv = []
                enum = 0
                for exp in DB["species"][SP]["sequences"][SEQ]["expressions"]:
                    expressioncsv.append(",".join([
                        str(enum),
                        arrows[exp["expression_level"]],
                        exp["FC"]  if exp["FC"] != "" else "<i class=\"uk-icon-ban uk-icon-medium\"></i>",
                        exp["methode"],
                        exp["tissue"],
                        gender[exp["gender"]],
                        exp["paper"],
                        exp["DOI"],
                        exp["note"],
                    ]).replace("\n","") )
                    enum += 1
                md_data["expressioncsv"] = "\n".join(expressioncsv)
                # write the yaml for hugo
                md = yaml.dump(md_data, allow_unicode=True,
                          default_flow_style=False,
                          explicit_start=True, explicit_end=True,
                          default_style="'", line_break="/n")[:-4]
                md += "---\n"
                f.write(md)

if __name__ == "__main__":
    DB = json.load(open("dist/sources.json"))
    export_browse(DB, "hugo_files/brows.csv")
    export_sequence_pages(DB, "../DormancyBase/content/sequence")
