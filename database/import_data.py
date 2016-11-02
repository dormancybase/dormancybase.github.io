import json
import sys

def process_species(in_file):
    species = []
    line_num = 1
    with open(in_file) as f:
        f.readline()
        for line in f:
            cells = line.strip().split("\t")
            if len(cells) < 6:
                print("colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
                continue
            species.append({
                "name": cells[1],
                "taxID": cells[2],
                "has_whole_genome": True if cells[3] == "1" else False,
                "dormancy_type": cells[4],
                "ordo": cells[5],
            })
            line_num +=1
    return species

def process_sequences(in_file):
    sequences = []
    line_num = 1
    with open(in_file) as f:
        f.readline()
        for line in f:
            cells = line.strip().split("\t")
            if len(cells) < 10:
                if len(cells) >= 5:
                    cells.extend(["","","","","","","",])
                else:
                    print("colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
                    continue
            sequences.append({
                "species": cells[1],
                "name": cells[2],
                "ncbi": cells[3],
                "type": cells[4],
                "note": cells[7],
                "other_id": cells[8],
                "other_id_type": cells[9],
            })
            line_num +=1
    return sequences

def process_expressions(in_file):
    expressions = []
    line_num = 1
    with open(in_file) as f:
        f.readline()
        for line in f:
            cells = line.strip().split("\t")
            if len(cells) < 11:
                print("colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
                continue
            expressions.append({
                "species": cells[1].split("---")[0],
                "name": cells[1].split("---")[1],
                "dormancy_type": cells[2],
                "life_stage": cells[3],
                "tissue": cells[4],
                "expression_level": cells[5],
                "FC": cells[6],
                "methode": cells[7],
                "DOI": cells[8],
                "paper": cells[9],
                "note": cells[10],
            })
            line_num +=1
    return expressions

def process_sources(json_file):
    out_json =  {
        "species": process_species("source/1_species_list.tsv"),
        "sequences": process_sequences("source/2_sequence_list.tsv"),
        "expressions": process_expressions("source/3_expression_list.tsv"),
    }
    with open(json_file, "w") as f:
        json.dump(out_json, f, indent=4)

if __name__ == "__main__":
    process_sources("dist/sources.json")
