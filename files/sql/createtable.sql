CREATE TABLE orders(
  PrimaryId integer primary key,
  Id VARCHAR(32),
  CurrencyPair VARCHAR(16),
  Direction VARCHAR(16),
  Status VARCHAR(16),
  OrderDate DATETIME,
  InitVolume FLOAT,
  InitPrice FLOAT,
  FillVolume FLOAT,
  FillPrice FLOAT,
  Tag VARCHAR(16),
  Description VARCHAR(255)
)