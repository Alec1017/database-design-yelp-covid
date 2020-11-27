import urllib
import json
url = 'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "695a8596-5458-442b-a017-7cd72471aade" where "ZIPCODE" like \'2108\' LIMIT 1'
url = 'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "695a8596-5458-442b-a017-7cd72471aade" where zipcode in ["2108", "2109", "2110", "2111", "2113", "2114", "2115", "2116", "2118", "2119", "2120", "2121", "2122", "2124", "2125", "2126", "2127", "2128", "2129", "2130", "2131", "2132","2134", "2135", "2136", "2151", "2152", "2163", "2199", "2203", "2210", "2215", "2467"] LIMIT 1'
url = 'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "695a8596-5458-442b-a017-7cd72471aade" where "ZIPCODE" in (\'2108\', \'2109\', \'2110\', \'2113\', \'2114\', \'2115\', \'2116\', \'2118\', \'2119\', \'2120\', \'2121\', \'2122\', \'2124\', \'2125\', \'2126\', \'2127\', \'2128\', \'2129\', \'2130\', \'2131\', \'2132\', \'2134\', \'2135\', \'2136\', \'2151\', \'2163\', \'2199\', \'2203\', \'2210\', \'2215\', \'2467\')'
fileobj = urllib.urlopen(url)
# print fileobj.read()
data = json.loads(fileobj.read())

all_results = []

records = data.get('result').get('records')

for record in records:

  if record.get('AV_TOTAL') == '0' or record.get('AV_TOTAL') == 0:
    continue

  json_result = {}

  json_result['property_id'] = record.get('PID', None)
  json_result['zip_code'] = '0' + record.get('ZIPCODE') if record.get('ZIPCODE') else None
  json_result['st_name'] = record.get('ST_NAME')
  json_result['st_num'] = record.get('ST_NUM')
  json_result['value'] = int(record.get('AV_TOTAL'))

  json_entry = json.dumps(json_result) 

  # Append the entry to the file
  with open("property_assessment2.json", "a") as outfile: 
    outfile.write("%s\n" % json_entry) 
  outfile.close()