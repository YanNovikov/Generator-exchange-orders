CREATE TABLE orders(
  primaryid integer primary key,
  ID VARCHAR(32),
  CurrencyPair VARCHAR(16),
  Direction VARCHAR(16),
  Status VARCHAR(16),
  OrderDate DATETIME,
  initVolume FLOAT,
  initPrice FLOAT,
  fillVolume FLOAT,
  fillPrice FLOAT,
  Tag VARCHAR(16),
  Description VARCHAR(255)
)