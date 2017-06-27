import csv
import re
import json
import us


def replace_right(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))

names_and_ids = {}

with open('usgs_list.tsv') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
    for row in reader:
        if row[2]:

            real_name = re.match('([^,]*)(.*)', row[2]).group(1)
            real_name = real_name.upper()
            
            for st in us.states.STATES:
                pattern = re.compile(r'\w*(' + st.abbr + ')$')
                
                real_name = re.sub(pattern, st.name.upper(), real_name) 

            real_name = real_name.replace(' R ', ' RIVER ')
            real_name = real_name.replace(' RV ', ' RIVER ')
            real_name = real_name.replace(' C ', ' CREEK ')
            real_name = real_name.replace(' CK ', ' CREEK ')
            real_name = real_name.replace(' STR ', ' STREAM ')
            real_name = real_name.replace(' FK ', ' FORK ')
            real_name = real_name.replace(' MF ', ' MIDDLE FORK ')
            real_name = real_name.replace(' M ', ' MIDDLE ')
            real_name = real_name.replace(' L. ', ' LOWER ')
            real_name = real_name.replace(' GL ', ' GLEN ')
            real_name = real_name.replace(' NR ', ' NEAR ')
            real_name = real_name.replace(' MI ', ' MILES ')
            real_name = real_name.replace(' ABV ', ' ABOVE ')
            real_name = real_name.replace(' AB ', ' ABOVE ')
            real_name = real_name.replace(' BCH. ', ' BEACH ')
            real_name = real_name.replace(' BLW ', ' BELOW ')
            real_name = real_name.replace(' CR ', ' CREEK ')
            real_name = real_name.replace(' DCH ', ' DITCH ')
            real_name = real_name.replace(' TRIB ', ' TRIBUTARY ')
            real_name = real_name.replace(' ST. ', ' STREET ')
            real_name = real_name.replace(' AVE. ', ' AVENUE ')
            real_name = real_name.replace(' CTY. ', ' COUNTY ')
            real_name = real_name.replace(' NO. ', ' NUMBER ')
            real_name = real_name.replace(' RD. ', ' ROAD ')
            real_name = real_name.replace(' NW ', ' NORTHWEST ')
            real_name = real_name.replace(' NE ', ' NORTHEAST ')
            real_name = real_name.replace(' SW ', ' SOUTHWEST ')
            real_name = real_name.replace(' SE ', ' SOUTHEAST ')
            real_name = real_name.replace(' N ', ' NORTH ')
            real_name = real_name.replace(' NO ', ' NORTH ')
            real_name = real_name.replace(' S ', ' SOUTH ')
            real_name = real_name.replace(' E ', ' EAST ')
            real_name = real_name.replace(' W ', ' WEST ')
            real_name = real_name.replace(' FT. ', ' FORT ')
            real_name = real_name.replace(' @HWY ', ' AT HIGHWAY ')
            real_name = real_name.replace(' @ ', ' AT ')
            real_name = real_name.replace(' UNNAMD ', ' UNNAMED ')
            real_name = real_name.replace(' SL ', ' SLOUGH ')
            real_name = real_name.replace(' ST. ', ' SAINT ')
            real_name = real_name.replace('\"', '')

            if (real_name not in names_and_ids):
                names_and_ids[real_name] = row[1]

with open('alexa_model.json') as json_data:
    d = json.load(json_data)

    value_string = '''
        {"id": null, "name": {"synonyms": [], "value": "Value 1"}}
    '''

    
    new_values_list = []
    for name, site_id in names_and_ids.items():
        value_json = json.loads(value_string)
        value_json["name"]["value"] = name
        value_json["id"] = site_id
        new_values_list.append(value_json)

    d['types'][0]['values'] = new_values_list

 #   print(json.dumps(d))
  
    print(json.dumps(new_values_list))