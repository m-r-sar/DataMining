import random
import time
import aiosqlite
import logging
import aiohttp
import asyncio

connection = None

async def init_db():
    global connection
    connection = await aiosqlite.connect("olxDB.db")
    logger.info("Database was successfully connected")

async def execute(query, vars = None):
    cursor = await connection.execute(query, vars)
    return await cursor.fetchone()

async def close_db():
    if connection:
        await connection.close()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.53', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:117.0) Gecko/20100101 Firefox/117.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:117.0) Gecko/20100101 Firefox/117.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15', 'Mozilla/5.0 (X11; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0', 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:115.0) Gecko/20100101 Firefox/115.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.51', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.51', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.53', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.83', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:118.0) Gecko/20100101 Firefox/118.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.52', 'Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.83', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0', 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0']
PROXY = ["proxies"]
AUTH = {'Proxy-Authorization': aiohttp.encode_basic_auth("login", "password")}
REGIONS = {"13": "if",  # Івано-Франківська область
           "24": "vin",  # Вінницька область
           "25": "ko",  # Київська область
           "6": "zht",  # Житомирська область
           "21": "dnp",  # Дніпропетровська область
           "5": "lv",  # Львівська область
           "9": "od",  # Одеська область
           "15": "pol",  # Полтавська область
           "8": "kha",  # Харківська область
           "23": "chn"} # Чернігівська область
OFFSETS = ["0", "50", "100", "150", "200", "250", "300", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800", "850", "900", "950", "1000"]
URL = "https://www.olx.ua/apigateway/graphql"
QUERY = """
query ListingSearchQuery(
  $searchParameters: [SearchParameter!] = []
  $fetchPayAndShip: Boolean = false
) {
  clientCompatibleListings(searchParameters: $searchParameters) {
    __typename
    ... on ListingSuccess {
      __typename
      data {
        _nodeId
        id
        location {
          city {
            id
            name
            normalized_name
            _nodeId
          }
          district {
            id
            name
            normalized_name
            _nodeId
          }
          region {
            id
            name
            normalized_name
            _nodeId
          }
        }
        last_refresh_time
        delivery {
          rock {
            active
            mode
            offer_id
          }
        }
        created_time
        category {
          id
          type
          _nodeId
        }
        contact {
          courier
          chat
          name
          negotiation
          phone
        }
        business
        omnibus_pushup_time
        photos {
          link
          height
          rotation
          width
        }
        promotion {
          highlighted
          top_ad
          options
          premium_ad_page
          urgent
          b2c_ad_page
        }
        protect_phone
        shop {
          subdomain
        }
        title
        status
        url
        user {
          id
          uuid
          _nodeId
          about
          b2c_business_page
          banner_desktop
          banner_mobile
          company_name
          created
          is_online
          last_seen
          logo
          logo_ad_page
          name
          other_ads_enabled
          photo
          seller_type
          social_network_account_type
          verification {
            status
          }
          businessProfiles {
            services {
              icon {
                url
                id
              }
              location {
                city
              }
              businessName
              foundationYear
              templateName
            }
          }
        }
        offer_type
        params {
          key
          name
          type
          value {
            __typename
            ... on GenericParam {
              key
              label
            }
            ... on CheckboxesParam {
              label
              checkboxParamKey: key
            }
            ... on PriceParam {
              value
              type
              negotiable
              label
              currency
              converted_value
              converted_currency
              arranged
              budget
            }
            ... on SalaryParam {
              from
              to
              arranged
              converted_currency
              converted_from
              converted_to
              currency
              gross
              type
            }
            ... on DynamicMultiChoiceCompatibilityListParam {
              __typename
            }
            ... on ErrorParam {
              message
            }
          }
        }
        description
        external_url
        partner {
          code
        }
        map {
          lat
          lon
          radius
          show_detailed
          zoom
        }
        safedeal {
          allowed_quantity
          weight_grams
        }
        valid_to_time
        isGpsrAvailable
        payAndShip @include(if: $fetchPayAndShip) {
          sellerPaidDeliveryEnabled
        }
      }
      metadata {
        filter_suggestions {
          clear_on_change
          break_line
          category
          label
          name
          type
          unit
          values {
            label
            value
          }
          constraints {
            type
          }
          search_label
          option {
            ranges
            order
            orderForSearch
            fakeCategory
          }
        }
        x_request_id
        search_id
        total_elements
        visible_total_count
        source
        search_suggestion {
          url
          type
          changes {
            category_id
            city_id
            distance
            district_id
            query
            region_id
            strategy
            excluded_category_id
          }
        }
        facets {
          category {
            id
            count
            label
            url
          }
          category_id_1 {
            count
            id
            label
            url
          }
          category_id_2 {
            count
            id
            label
            url
          }
          category_without_exclusions {
            count
            id
            label
            url
          }
          category_id_3_without_exclusions {
            id
            count
            label
            url
          }
          city {
            count
            id
            label
            url
          }
          district {
            count
            id
            label
            url
          }
          owner_type {
            count
            id
            label
            url
          }
          region {
            id
            count
            label
            url
          }
          scope {
            id
            count
            label
            url
          }
        }
        new
        promoted
      }
      links {
        first {
          href
        }
        next {
          href
        }
        previous {
          href
        }
        self {
          href
        }
      }
    }
    ... on ListingError {
      __typename
      error {
        code
        detail
        status
        title
        validation {
          detail
          field
          title
        }
      }
    }
  }
}
"""

async def get_item_data(item):
    id = int(item.get("id", None))

    exists = await execute("SELECT 1 FROM listing WHERE id = ?", (id,))
    if exists:
        return None

    title = item.get("title", None)
    url = item.get("url", None)
    description = item.get("description", None)

    params = item.get("params", None)

    price_info = params[0].get("value", None)
    price_value = float(price_info.get("value", None))
    price_currency = price_info.get("currency", None)
    price_uah = price_info.get("converted_value", None)
    if price_uah:
        price_uah = float(price_uah)

    etc = {}
    for param in params[1:]:
        etc[param["key"]] = param.get("value", None).get("key", param.get("value", None).get("checkboxParamKey", None))

    for e in etc:
        if type(etc[e]) == list:
            etc[e] = ", ".join(etc[e])


    location = item.get("location", None)


    city = location.get("city", None)
    region = location.get("region", None)
    district = location.get("district", None)

    if city:
        city_id = int(city.get("id", None))
        city_name = city.get("name", None)
        city_normalized_name = city.get("normalized_name", None)
    else:
        city_id = None
        city_name = None
        city_normalized_name = None

    if region:
        region_id = int(region.get("id", None))
        region_name = region.get("name", None)
        region_normalized_name = region.get("normalized_name", None)
    else:
        region_id = None
        region_name = None
        region_normalized_name = None

    if district:
        district_id = int(district.get("id", None))
        district_name = district.get("name", None)
        district_normalized_name = district.get("normalized_name", None)
    else:
        district_id = None
        district_name = None
        district_normalized_name = None

    created_time = item.get("created_time", None)
    last_refresh_time = item.get("last_refresh_time", None)

    photos = item.get("photos", None)
    if photos:
        photos_links = [photo.get("link").split(";")[0] for photo in photos]
    else:
        photos_links = []

    data = [id, title, url, description, price_value, price_currency, price_uah, city_id, city_name, city_normalized_name, region_id, region_name, region_normalized_name, district_id, district_name, district_normalized_name, created_time, last_refresh_time]
    return data, photos_links, etc


async def commit_item(data, photos_links, etc):
    id = data[0]
    columns = ('title', 'url', 'description', 'price_value', 'price_currency', 'price_uah', 'city_id', 'city_name', 'city_normalized_name', 'region_id', 'region_name', 'region_normalized_name', 'district_id', 'district_name', 'district_normalized_name', 'created_time', 'last_refresh_time')

    await execute("INSERT OR IGNORE INTO listing(id) VALUES (?)", (id,))

    for col, value in zip(columns, data[1:]):
        if value is None:
            await execute(f"UPDATE listing SET {col} = NULL WHERE id = ?", (id,))
        else:
            await execute(f"UPDATE listing SET {col} = ? WHERE id = ?", (value, id))

    if photos_links:
        photos = [(id, link) for link in photos_links]
        for photo in photos:
            await execute("INSERT OR IGNORE INTO photos VALUES (?, ?)", photo)

    for param in etc:
        await execute(f"UPDATE listing SET {param} = ? WHERE id = ?", (etc[param], id))




async def scrap_region(region, offset, sem, tries = 0):
    async with sem:
        while tries < 10:
            logger.info(f"-- Scrapping with offset {offset} --")
            variables = {
                "searchParameters": [
                    {
                        "key": "offset",
                        "value": offset
                    },
                    {
                        "key": "limit",
                        "value": "50"
                    },
                    {
                        "key": "category_id",
                        "value": "1758"
                    },
                    {
                        "key" : "region_id",
                        "value" :  region
                    }
                ],
                "fetchPayAndShip": False
            }
            headers = {
                'accept': 'application/json',
                # 'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'uk',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'origin': 'https://www.olx.ua',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': f'https://www.olx.ua/uk/nedvizhimost/kvartiry/{REGIONS[region]}/?currency=UAH',
                'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': random.choice(USER_AGENTS),
                'x-client': 'DESKTOP'
            }

            payload = {"query" : QUERY,
                        "variables" : variables}
            try:
                session.cookie_jar.clear()
                async with session.post(URL, json=payload, headers=headers, proxy=random.choice(PROXY), proxy_headers=AUTH) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data["data"]["clientCompatibleListings"]["data"]
                        for item in items:
                            try:
                                result = await get_item_data(item)
                                if result:
                                    info, photos_links, etc = result
                                    await commit_item(info, photos_links, etc)

                            except Exception as e:
                                logger.error(f"Could not get item data for region. Exception: {e}, Item: {item}")
                        await connection.commit()
                        break


                    elif response.status == 403 or response.status == 429:
                        logger.warning(f"OLX blocked connection for that proxy, status code: {response.status}")
                        tries += 1
                        if tries > 5:
                            time.sleep(random.uniform(4, 10))
                    else:
                        logger.warning(f"Request failed with status code {response.status}")
            except aiohttp.client_exceptions.ClientHttpProxyError as e:
                logger.error(f"Request to proxy failed with: {e.status}. Waiting for a 60s")
                await asyncio.sleep(60)
            except aiohttp.client_exceptions.ClientConnectorError as e:
                logger.error(f"Request to OLX failed with: {e}. Waiting for a 30s")
                await asyncio.sleep(30)
            except aiohttp.client_exceptions.ConnectionTimeoutError as e:
                logger.error(f"Request to OLX timeout with: {e}. Waiting for a 30s")
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Somehow request to OLX failed with: {e}. Just to be safe waiting for a 30s")
                await asyncio.sleep(30)

async def main():
    await init_db()

    global session
    global sem

    session = aiohttp.ClientSession()
    sem = asyncio.Semaphore(10)

    for region in REGIONS:
        await asyncio.sleep(random.uniform(8, 10))
        logger.info(f"===== SCRAPPING REGION: {region} : {REGIONS[region]} =====")

        tasks = [scrap_region(region, offset, sem) for offset in OFFSETS]

        await asyncio.gather(*tasks)

    await close_db()

if __name__ == '__main__':
    asyncio.run(main())