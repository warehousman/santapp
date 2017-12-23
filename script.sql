CREATE TABLE santa
(
  name      TEXT,
  uuid      UUID DEFAULT uuid_generate_v1() NOT NULL
    CONSTRAINT claus_uuid_pk
    PRIMARY KEY,
  party     TEXT,
  has_party BOOLEAN,
  real_name TEXT
);


