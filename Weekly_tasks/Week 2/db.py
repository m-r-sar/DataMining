import sqlite3

connection = sqlite3.connect("olxDB.db")

cursor = connection.cursor()

cursor.execute("""
    create table listing(
    id                             INTEGER
        primary key,
    title                          TEXT,
    url                            TEXT,
    description                    TEXT,
    price_value                    REAL,
    price_currency                 TEXT,
    price_uah                      REAL,
    city_id                        INTEGER,
    city_name                      TEXT,
    city_normalized_name           TEXT,
    region_id                      INTEGER,
    region_name                    TEXT,
    region_normalized_name         TEXT,
    district_id                    INTEGER,
    district_name                  TEXT,
    district_normalized_name       TEXT,
    created_time                   TEXT,
    last_refresh_time              TEXT,
    apartments_object_type         TEXT,
    commission                     TEXT,
    property_type_appartments_sale TEXT,
    zkh                            TEXT,
    floor                          TEXT,
    total_floors                   TEXT,
    total_area                     TEXT,
    contract_type                  TEXT,
    kitchen_area                   TEXT,
    house_type                     TEXT,
    apartments_dev_type            TEXT,
    number_of_rooms_string         TEXT,
    bathroom                       TEXT,
    heating                        TEXT,
    repair                         TEXT,
    furnish                        TEXT,
    appliances                     TEXT,
    multimedia_2                   TEXT,
    comfort                        TEXT,
    communications                 TEXT,
    ecosystem_1_km                 TEXT,
    cooperate                      TEXT,
    year_of_commissioning          TEXT,
    layout                         TEXT,
    infrastructure_500_m           TEXT,
    is_exchange                    TEXT,
    eoselia                        TEXT,
    inclusiveness                  TEXT
);
""")

cursor.execute("""
    create table photos(
    id         INTEGER,
    photo_link TEXT
);
""")

connection.commit()
