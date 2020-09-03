import json
import logging
import os
import ssl
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

MAX_RESULTS = None


def fetch_url_json_batched(url, max_results=MAX_RESULTS):
    logging.info('Fetching JSON data from {}'.format(url))

    results = []
    start = 0

    while True:
        batch = _fetch_batch(url, start, max_results)

        results.extend(batch)

        if not batch:
            break

        start += len(batch)

    logging.info('JSON data fetched. {} items'.format(len(results)))

    return results


def _fetch_batch(url, start, max_results, abort_on_429=False):
    logging.info(
        'Fetching items starting at {}'.format(start)
    )

    url += '?start={}'.format(start)

    if max_results is not None:
        url += '&maxResults={}'.format(max_results)

    request = Request(url)

    request.add_header('Ocp-Apim-Subscription-Key', os.environ['VINMONOPOLET_API_KEY'])

    try:
        response = urlopen(request, context=ssl._create_unverified_context())
    except HTTPError as exception:
        if exception.code == 400:
            return []
        elif exception.code == 429:
            if abort_on_429:
                logging.error('Hit daily limit. Aborting')

                raise exception

            logging.warn('Hit minute limit. Waiting 60 seconds for retry')

            time.sleep(61)

            return _fetch_batch(url, start, max_results, abort_on_429 = True)
        else:
            raise exception

    return json.loads(response.read())
