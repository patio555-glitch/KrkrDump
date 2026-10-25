"""Generate candidate file names for the nameList option.

Usage:
    python make_names.py OUT.txt --prefixes noa,ama --pattern "{p}_loop_{n:03d}" --count 1000 --exts .ogg,.ogg.sli

--pattern is a str.format template; {p} is the prefix and {n} the counter (0 .. count-1).
Add several --pattern options to combine schemes. Without {n}, the name is written once per prefix.
"""
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--prefixes", required=True, help="comma separated")
    ap.add_argument("--pattern", action="append", required=True)
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--exts", default=".ogg", help="comma separated")
    args = ap.parse_args()

    prefixes = [p for p in args.prefixes.split(",") if p]
    exts = [e for e in args.exts.split(",") if e]
    names = []

    for pattern in args.pattern:
        counted = "{n" in pattern

        for p in prefixes:
            for n in range(args.count if counted else 1):
                base = pattern.format(p=p, n=n)
                names.extend(base + e for e in exts)

    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(names) + "\n")

    print(len(names), "names ->", args.out)


if __name__ == "__main__":
    main()
