import json
import sys

def update_seq_id(SEQ_ID_file, in_file):
    try:
        SEQ_ID = json.load(open(SEQ_ID_file))
    except FileNotFoundError:
        SEQ_ID = {"ID":{}, "name2ID": {}, "ncbi2ID": {}, "other2ID": {}, "nextID": 0}
    with open(in_file) as f:
        f.readline()
        for line in f:
            cells = line.strip().split("\t")
            if len(cells) < 10:
                if len(cells) >= 5:
                    cells.extend(["","","","","","","",])
                else:
                    print("ERROR: colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
                    continue
            if cells[2].lower() not in SEQ_ID["name2ID"]:
                SID = 'DB_SEQ{:06d}'.format(SEQ_ID["nextID"])
                SEQ_ID["nextID"] += 1
                SEQ_ID["ID"][SID] = {
                    "species": cells[1],
                    "name": cells[2].lower(),
                    "ncbi": cells[3].lower(),
                    "other_id": cells[8].lower(),
                    "other_id_type": cells[9].lower(),
                }
                SEQ_ID["name2ID"][cells[2].lower()] = SID
                if cells[3] != "":
                    SEQ_ID["ncbi2ID"][cells[3].lower()] = SID
                if cells[8] != "":
                    SEQ_ID["other2ID"][cells[8].lower()] = SID
    with open(SEQ_ID_file, "w") as f:
        json.dump(SEQ_ID, f, indent=4)

def process_species(in_file):
    species = []
    line_num = 1
    with open(in_file) as f:
        f.readline()
        for line in f:
            cells = line.strip().split("\t")
            if len(cells) < 6:
                print("ERROR: colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
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
                    print("ERROR: colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
                    continue
            sequences.append({
                "species": cells[1],
                "name": cells[2].lower(),
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
                print("ERROR: colnum error!!! %s:%s: %s" % (in_file, line_num, line), file=sys.stderr)
                continue
            expressions.append({
                "species": cells[1].split("---")[0],
                "name": cells[1].split("---")[1].lower(),
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

def process_sources(SEQ_ID_file, species_list, sequence_list, expression_list):

    SEQ_ID = json.load(open(SEQ_ID_file))
    DB = {
        "species": {},
        "sequences": {},
        "expressions": {},
        "relations": {},
    }

    # process species
    DB["relations"]["spname2taxid"] = {}
    for sp in process_species(species_list):
        DB["species"][sp["taxID"]] = {
            "name": sp["name"],
            "has_whole_genome": sp["has_whole_genome"],
            "dormancy_type": sp["dormancy_type"],
            "ordo": sp["ordo"],
            "sequences": {},
            "life_stage": "",
        }
        DB["relations"]["spname2taxid"][sp["name"]] = sp["taxID"]

    # process sequences
    DB["relations"]["seqid2sp"] = {}
    Snum = 0
    for seq in process_sequences(sequence_list):
        SID = SEQ_ID["name2ID"][seq["name"]]
        Snum += 1
        try:
            Ssp = DB["relations"]["spname2taxid"][seq["species"]]
        except KeyError:
            print("ERROR: unknown species!!! %s %s" % (seq["name"], seq["species"]), file=sys.stderr)
            continue
        DB["species"][Ssp]["sequences"][SID] = {
            "innerID": SID,
            "species": Ssp,
            "name": seq["name"],
            "ncbi": seq["ncbi"],
            "type": seq["type"],
            "note": seq["note"],
            "other_id": seq["other_id"],
            "other_id_type": seq["other_id_type"],
            "expressions" : [],
            "life_stage": "",
        }
        DB["relations"]["seqid2sp"][SID] = Ssp

    # process expressions
    Enum = 0
    for exp in process_expressions(expression_list):
        EID = 'DB_E_{:06d}'.format(Enum)
        Enum += 1
        try:
            Eseq = SEQ_ID["name2ID"][exp["name"]]
        except KeyError:
            print("ERROR: unknown sequence in expression list!!! %s" % (exp["name"]), file=sys.stderr)
            continue
        try:
            Esp = DB["relations"]["seqid2sp"][Eseq]
        except KeyError:
            print("ERROR: unknown species in expression list!!! %s %s" % (exp["name"], exp["species"]), file=sys.stderr)
            continue
        DB["species"][Esp]["sequences"][Eseq]["expressions"].append({
            "ID": EID,
            "species": Esp,
            "dormancy_type": exp["dormancy_type"],
            "life_stage": exp["life_stage"] if exp["life_stage"] != "" else None,
            "tissue": exp["tissue"],
            "expression_level": exp["expression_level"],
            "FC": exp["FC"],
            "methode": exp["methode"],
            "DOI": exp["DOI"],
            "paper": exp["paper"],
            "note": exp["note"],
        })

    # check expression for sequnces:
    del_seq = {}
    for sp in DB["species"]:
        del_seq[sp] = []
        for seq in DB["species"][sp]["sequences"]:
            if len(DB["species"][sp]["sequences"][seq]["expressions"]) == 0:
                print("WARNING: there aren't any expression data for: %s" % (DB["species"][sp]["sequences"][seq]["name"]), file=sys.stderr)
                del_seq[sp].append(seq)
    # del sequences without expression
    for sp in del_seq:
        for seq in del_seq[sp]:
            del(DB["species"][sp]["sequences"][seq])

    # filter life stage for sequences
    for sp in DB["species"]:
        for seq in DB["species"][sp]["sequences"]:
            ls = list(set([ e["life_stage"] for e in DB["species"][sp]["sequences"][seq]["expressions"] if e["life_stage"]]))
            if len(ls) > 1:
                print("Warning: there aren't many life_stage for sequence: %s, %s" % (DB["species"][sp]["sequences"][seq]["name"], ls), file=sys.stderr)
                DB["species"][sp]["sequences"][seq]["life_stage"] = " / ".join(ls)
            elif len(ls) == 0:
                DB["species"][sp]["sequences"][seq]["life_stage"] = ""
            else:
                DB["species"][sp]["sequences"][seq]["life_stage"] = ls[0]

    # filter life stage for species
    for sp in DB["species"]:
        ls = list(set([ DB["species"][sp]["sequences"][e]["life_stage"] for e in DB["species"][sp]["sequences"] if DB["species"][sp]["sequences"][e]["life_stage"]]))
        if len(ls) > 1:
            print("Warning: there aren't many life_stage for species: %s, %s" % (DB["species"][sp]["name"], ls), file=sys.stderr)
            DB["species"][sp]["life_stage"] = " / ".join(ls)
        elif len(ls) == 0:
            DB["species"][sp]["life_stage"] = ""
        else:
            DB["species"][sp]["life_stage"] = ls[0]

    # return with the database
    return DB

if __name__ == "__main__":
    SEQ_ID_file = "DormancyBaseID.json"
    source_species_file = "source/1_species_list.tsv"
    source_sequence_file = "source/2_sequence_list.tsv"
    source_expression_file = "source/3_expression_list.tsv"
    update_seq_id(SEQ_ID_file, source_sequence_file)
    DB = process_sources(
        SEQ_ID_file,
        source_species_file,
        source_sequence_file,
        source_expression_file)
    with open("dist/sources.json", "w") as f:
        json.dump(DB, f, indent=4)
