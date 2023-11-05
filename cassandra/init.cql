CREATE KEYSPACE urlshortener
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 2
};


CREATE TABLE urlshortener.urls (
    short_url text PRIMARY KEY,
    long_url text
);
