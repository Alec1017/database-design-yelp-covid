import os
import json
import requests
from dotenv import load_dotenv

from boston_locations import boston_locations

load_dotenv()


def get_boston_business_ids():
  endpoint = 'https://api.yelp.com/v3/businesses/search'
  headers = {'Authorization': 'bearer %s' % os.getenv('API_KEY')}

  offset_increment = 50
  total_queries = 0
  total_businesses_retrieved = 0
  all_business_ids = set()

  print "Starting Yelp API search..."

  # Gets all businesses in Boston using long/lat
  for location in boston_locations:

    offset = 0
    offset_increment = 50
    longitude = location.get('longitude')
    latitude = location.get('latitude')
    radius = location.get('radius')
    last_query = False

    while offset <= 900:

      # query the api with the current offset
      params = {'latitude': latitude, 'longitude': longitude, 'limit': 50, 'offset': offset, 'sort_by': 'distance'}
      response = requests.get(url=endpoint, headers=headers, params=params)
      business_data = response.json()

      # get all IDs
      for business in business_data.get('businesses'):
        all_business_ids.add(business.get('id'))
        total_businesses_retrieved += 1

      # break out of the while loop if this is the last query
      if last_query:
        break

      # make sure we know what the limit is, if its less than 1000
      if (int(business_data.get('total')) - offset) < offset_increment:
        offset_increment = int(business_data.get('total')) - offset
        last_query = True

      # increment totals
      offset += offset_increment
      total_queries += 1

    print "total retrieved so far: %s" % len(all_business_ids)


  # append them to a text file  
  with open("all_business_ids.txt", "w") as writer:
    for business_id in list(all_business_ids):
      writer.write(business_id + '\n')
  writer.close()

  print "retrieved all businesses in boston!"
  print "total businesses found, counting duplicated: %s" % total_businesses_retrieved
  print "total unique businesses found: %s" % len(all_business_ids)
  print "total queries used: %s" % total_queries


def build_categories(categories):
  return ", ".join([category.get('title') for category in categories])


def query_each_business(start_at=None, data_file="all_business_ids.txt"):
  business_ids = open(data_file).read().splitlines()

  if start_at:
    business_ids = business_ids[start_at:]

  # test_business_ids = business_ids[0:5] 
  headers = {'Authorization': 'bearer %s' % os.getenv('API_KEY')}
  count = 0

  # Query each business in our file
  for business_id in business_ids:
    endpoint = 'https://api.yelp.com/v3/businesses/%s' % business_id
    json_object = {}

    # query the business
    response = requests.get(url=endpoint, headers=headers)
    business_data = response.json()

    # build up json object
    json_object['restaurant_id'] = business_data.get('id', None)
    json_object['restaurant_name'] = business_data.get('name', None)
    json_object['zip_code'] = business_data.get('location').get('zip_code', None) if business_data.get('location') else None
    json_object['star_rating'] = business_data.get('rating', None)
    json_object['num_reviews'] = business_data.get('review_count', None)
    json_object['cuisine'] = build_categories(business_data.get('categories')) if business_data.get('categories') else None
    json_object['latitude'] = business_data.get('coordinates').get('latitude', None) if business_data.get('coordinates') else None
    json_object['longitude'] = business_data.get('coordinates').get('longitude', None) if business_data.get('coordinates') else None
    json_object['is_closed'] = 1 if business_data.get('is_closed') else 0
    json_object['transactions'] = ", ".join(business_data.get('transactions')) if business_data.get('transactions') else None

    json_entry = json.dumps(json_object) 

    # Append the entry to the file
    with open("business_data.json", "a") as outfile: 
      outfile.write("%s\n" % json_entry) 
    outfile.close()

    # do some counting output
    count += 1
    if count % 500 == 0:
      print "queried so far: %s" % count


# Run the query
if __name__=="__main__": 
    #get_boston_business_ids() 
    query_each_business()

