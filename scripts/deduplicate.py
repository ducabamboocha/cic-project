import json


def main():

    with open('homegate.jsonl', 'r') as f:
        homegate_data = [json.loads(d) for d in f.readlines()]

    with open('immoscout.jsonl', 'r') as f:
        immoscout_data = [json.loads(d) for d in f.readlines()]

    final_dict = {}

    for d in homegate_data:
        if d['title'] not in final_dict:
            final_dict[d['title']] = [{"platform": "homegate", "id": d["id"]}]
        else:
            final_dict[d['title']].append({"platform": "homegate", "id": d["id"]})

    for d in immoscout_data:
        if d['title'] not in final_dict:
            final_dict[d['title']] = [{"platform": "immoscout", "id": d["id"]}]
        else:
            final_dict[d['title']].append({"platform": "immoscout", "id": d["id"]})

    res = [d for d in list(final_dict.values()) if len(d) > 1]

    with open('result.json', 'w') as f:
        f.write(str(res))


if __name__ == '__main__':
    main()
    print("DONE DEDUPLICATE")