import os
import json
import requests
from dotenv import load_dotenv

from boston_locations import boston_locations

load_dotenv()

endpoint = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % os.getenv('API_KEY')}


def get_boston_business_ids(endpoint, headers):
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
      params = {'latitude': latitude, 'longitude': longitude, 'limit': 50, 'offset': offset}
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


# Run the query
if __name__=="__main__": 
    get_boston_business_ids(endpoint, headers) 

