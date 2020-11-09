import json
import os
import sys

header = ["race_id", "fips", "name", "votes", "absentee_votes", "reporting", "precincts", "eevp", "tot_exp_vote", "eevp_value", "eevp_display", "eevp_source", "turnout_stage", "absentee_count_progress", "absentee_outstanding",
          "absentee_max_ballots", "provisional_outstanding", "provisional_count_progress", "results-trumpd", "results-bidenj", "results-jorgensenj", "results-venturaj", "results-pierceb", "results-blankenshipd", "results-de_la_fuenter",
          "results-write-ins", "results_absentee-trumpd", "results_absentee-bidenj", "results_absentee-jorgensenj", "results_absentee-venturaj", "results_absentee-pierceb", "results_absentee-blankenshipd", "results_absentee-de_la_fuenter",
          "results_absentee-write-ins", "last_updated", "leader_margin_value", "leader_margin_display", "leader_margin_name_display", "leader_party_id", "margin2020"]


def make_csv(json_path, csv_path):
    print(",".join(header))

    with open(json_path) as json_file:
        data_json = json.load(json_file)
        data = data_json['data']['races']

        with open( csv_path , 'w') as csv_file:

            csv_file.write(','.join(header))
            csv_file.write('\n')

            for race in data:
                raceId = race["race_id"]
                counties = race["counties"]

                for county in counties:
                    entry = []
                    entry.append(raceId)
                    for key in header[1:]:
                        if not "-" in key:
                            entry.append(str(county[key]))
                        else:
                            key1 = key[0:key.index("-")]
                            key2 = key[key.index("-") + 1:]
                            if (key1 in county and key2 in county[key1]):
                                entry.append(str(county[key1][key2]))
                            else:
                                entry.append("")
                    for entity in entry:
                        if "," in entity:
                            raise Exception("There is a comma in the data")
                    line = ",".join(entry)
                    csv_file.write(line)
                    csv_file.write('\n')


if __name__ == '__main__':
    json_path = '../data/results.json'
    csv_path  = '../output/results.csv'

    # csv_path = os.path.join(os.path.dirname(json_path), os.path.splitext(json_path)[0] + '.csv')

    make_csv(json_path, csv_path)
