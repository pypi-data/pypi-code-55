#!/usr/bin/python3

import sys
import json
import aimslib.detailed_roster.process as process
import aimslib.common.types as T

if __name__ == "__main__":
    raw_roster = open(sys.argv[1]).read()
    duties = process.duties(raw_roster)
    crews = process.crew(raw_roster)
    for d in duties:
        print(json.dumps(d, default=lambda o: str(o), indent=2))
        sectors = [X for X in d.sectors
                   if d.sectors and X.flags == T.SectorFlags.NONE]
        for s in sectors:
            if (s.crewlist_id not in crews and
                f"{s.crewlist_id[:8]}All~" in crews):
                crews[s.crewlist_id] = crews[f"{s.crewlist_id[:8]}All~"]
            print(f"{s.sched_start} {s.from_}/{s.to}")
            for cm in crews[s.crewlist_id]:
                print(f"  {cm.role}: {cm.name}")
    # # print("Output as lines:")
    # l = process.lines(raw_roster)
    # # for line in l:
    # #     print("  ", len(line), [X.replace(" ", " ") for X in line])
    # # print("\nOutput as columns:")
    # cols = process.columns(l)
    # for c in cols:
    #     print("  ", len(c), c)
    # # print("\nOutput as event stream:")
    # es = process.event_stream(process.extract_date(l), cols)
    # # for e in es:
    # #     print("  ", e)
    # print("\nOutput as duty stream:")
    # ds = process.duty_stream(es)
    # for d in ds:
    #     print("  ", [str(X) for X in d])

    # print("Table extraction")
    # print("================")
    # table = process.extract_table(raw_roster)
    # for t in table:
    #     print(t[0], "[%s - %s]" % tuple(t[1]))
    #     for ev in t[2:]:
    #         for d in ev:
    #             print("   [%s]" % d)
    #         print()
    # print("Crew extraction")
    # print("===============")
    # crew = extract_crew(raw_roster)
    # ck = list(crew.keys())
    # ck.sort()
    # for k in ck:
    #     print(k, crew[k])
