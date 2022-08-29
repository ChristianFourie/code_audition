"""
The Asteroid Tracker program
"""

import logging
import requests


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


API_URL = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=%s&end_date=%s&api_key=DEMO_KEY'


def main():
    """
    Main function which parses input and calculates statistics.
    """

    start_date = None
    end_date = None

    # TODO: Task 1 - Gather user input

    start_date = input("Please provide a start date (eg. 2021-02-12): ") #'2021-01-01'#
    end_date = input("Please provide a end date (eg. 2021-02-12): ")

    stats = calculate_statistics(start_date, end_date)

    print_statistics(stats)


def calculate_statistics(start_date, end_date):
    """
    Make an API request and calculate statistics.
    """

    # TODO: Task 2 - Prepare and make the HTTP request

    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    url = API_URL % (start_date, end_date)

    print("Please wait, fetching data...")
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:

        # TODO: Task 3 - Calculate statistics

        num_asteroids = data['element_count']
        num_potentially_hazardous_asteroids = 0
        list_largest_diameter_meters = []
        list_nearest_miss_kms = []
        largest_diameter_meters = -1
        nearest_miss_kms = -1

        keysList = list(data['near_earth_objects'].keys())

        for detected_date in keysList:
            objects_for_date = data['near_earth_objects'][detected_date]
            for detected_object in objects_for_date:
                if detected_object['is_potentially_hazardous_asteroid']:
                    num_potentially_hazardous_asteroids += 1

                list_largest_diameter_meters.append(detected_object['estimated_diameter']['meters']['estimated_diameter_max'])
                list_nearest_miss_kms.append(float(detected_object['close_approach_data'][0]['miss_distance']['kilometers']))

        largest_diameter_meters = max(list_largest_diameter_meters)
        nearest_miss_kms = min(list_nearest_miss_kms)

        return {
            'start_date': start_date,
            'end_date': end_date,
            'num_asteroids': num_asteroids,
            'num_potentially_hazardous_asteroids': num_potentially_hazardous_asteroids,
            'largest_diameter_meters': largest_diameter_meters,
            'nearest_miss_kms': nearest_miss_kms,
        }

    else:
        return {
            'error': {
                'code': data['code'],
                'type': data['http_error'],
                'message': data['error_message']
            }
        }


def print_statistics(stats):
    """
    Print the calculated statistics.
    """

    logger.info('')

    if 'error' in stats:
        logger.error('HTTP Error:')
        logger.error('Code: %s', stats['error']['code'])
        logger.error('Type: %s', stats['error']['type'])
        logger.error('Message: %s', stats['error']['message'])

    else:
        logger.info('Displaying asteroid data for period %s - %s' % (stats['start_date'], stats['end_date']))
        logger.info('---------------------------------------------------------------------')
        logger.info('Number of asteroids: %d' % stats['num_asteroids'])
        logger.info('Number of potentially hazardous asteroids: %d' % stats['num_potentially_hazardous_asteroids'])
        logger.info('Largest estimated diameter: %f m' % stats['largest_diameter_meters'])
        logger.info('Nearest miss: %f km' % stats['nearest_miss_kms'])

    logger.info('')


if __name__ == '__main__':
    main()
