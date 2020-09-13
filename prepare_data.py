import argparse
import wikipedia

collected_terms = []


def collect_for_term(term, ignore_links=[]):

    global collected_terms

    cnts = list()

    p = wikipedia.page(term)

    cnts.append(p.content)

    for link in p.links:
        if link in ignore_links or link.replace(".", "").isnumeric() or link in collected_terms:
            continue

        try:
            print("link: ", link)
            pl = wikipedia.page(link)
            cnts.append("=== " + link + " ===")
            cnts.append(pl.content)

            collected_terms.append(link)
        except Exception as e:
            print(e)
    return cnts


def collect(args):

    contents = list()

    wikipedia.set_lang(args.lang)

    for term in args.terms:
        contents.extend(collect_for_term(term))

    # Write out
    print("Saving to: ", args.output)
    with open(args.output, "w") as fh:
        out = "\n".join(contents)
        fh.write(out)


def collect_f1():
    contents = list()

    wikipedia.set_lang("hr")

    ignore_links = ['21. stoljeće', 'Drugi svjetski rat', 'Europa', 'Europska unija', 'Indija', 'Italija', 'JAR', 'Kina', 'Meksiko', 'Rusija', 'Turska', 'Ujedinjeno Kraljevstvo']
    contents.extend(collect_for_term("Formula 1", ignore_links))
    contents.extend(collect_for_term("Dodatak:Popis vozača u Formuli 1"))
    contents.extend(collect_for_term("Dodatak:Popis staza Formule 1"))
    contents.extend(collect_for_term("Dodatak:Popis konstruktora u Formuli 1"))
    contents.extend(collect_for_term("Popis Velikih nagrada Formule 1"))

    # Write out
    with open("__old/data/f1.txt", "w") as fh:
        out = "\n".join(contents)
        out = out.replace("räikkönen", "raikkonen").replace("Räikkönen", "Raikkonen")
        fh.write(out)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", help="Enter delimited list of terms", type=str)
    parser.add_argument("--lang", help="Enter language of wikipedia", default="hr")
    parser.add_argument("--output", help="Output file", default="./data/output.txt")
    args = parser.parse_args()
    args.terms = args.terms.split(",")

    collect(args)
