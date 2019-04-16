# Exchange orders history generator
It generates orders according to defined rules. You can change configuration if you want.
Insert what you made into a database table. Customize objects that you generate.
Clone this repository:

```bash
$ git clone https://github.com/YanNovikov/Generator-exchange-orders.git
```

Additional modules:
```bash
$ pip install -r /path/to/project/folder/requirements.txt 
```

Meet, exchange order
--
Orders are divided on three parts:
* Orders witch are completed between two dates (Red zone)
* Orders witch have all life cycle in dates (Green zone)
* And last are only started in this period (Blue zone)

Single order row contains

```
    ID - Unique id (15 digits)
    Direction - Buy or Sell
    Currencypair - Name of currency pairs
    Price - Price of currency pair
    Volume - Initial volume
    Status - Shows order state
    Orderdate - Date and time of this order state
    Tag - A little information about order
```

You can set period of trading in your configuration. Example is defaults.json in dirrectory files/

---
#How to use?
Create database and table according to orders fields

Then write all fields of configurations according to defaults.json

```
{
  "datafilename": "files/orders",
  "orderscount": 300,
  "batchcount": 3,
  "redpart": 0.15,
  "greenpart": 0.60,
  "bluepart": 0.25,
  "startdate": "12.03.2019 00:00:00",
  "finishdate": "20.03.2019 00:00:00",
  "status": ["New", "To-provider", "Filled", "Partial-filled", "Reject"],
  "currencypairs": ["EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF",
                 "AUD/USD", "USD/CAD", "NZD/USD", "EUR/GBP",
                 "EUR/JPY", "EUR/CHF", "GBP/JPY", "AUD/JPY",
                 "NZD/JPY", "AUD/EUR", "NZD/EUR", "EUR/CAD"],
  "tags": ["Home", "LinkedIn", "Facebook", "BitBon", "Repairs", "Academy", "Apple", "Green Peace"],
  "dirrection": ["Buy", "Sell"],
  "maxpx": 10,
  "minpx": 1,
  "maxvol": 100,
  "minvol": 10,

  "dbname": "generator",
  "tablename": "orders",
  "user": "root",
  "password": "12345678",
  "host": "localhost",
  "createtablefile": "files/createtable.sql",
  "testselect": "SELECT * FROM Orders",

  "queuename": "orders"
}
```


## Start app

```
$ python launcher.py -c --loggermode=info --configs customconfigs.json
```

--loggermode it is a level of output logs. Can be: trace, debug, info, warning, error, critical, fatal.

-f file writing logs.

-c console writing logs.

--configs is a path to your config file.

All options are not required.
By default is info level, console and file writing, defaults.json


---
## See result
```bash
$ python launcher.py customconfigs.json INFOWARNING
[INFO]: Logger started in default mode.
[INFO]: Logger mode is now set in INFOWARNING.
[INFO]: Loading configs from files/defaults.json.
[INFO]: Loading configs from files/customconfigs.json.
[INFO]: Configurations for generating loaded.
[INFO]: Configurations for database usage loaded.
[INFO]: Configurations for messaging loaded.
[INFO]: Orders created: 300.
[INFO]: All rows successfully added to file files/orders.
[INFO]: Connection to database 'generator' is Success.
[INFO]: All records from table 'orders' have been deleted.
[INFO]: All rows from file have bean inserted into a table - Success.
[INFO]: Changes are successfully commited.
[INFO]: Report is made in file files/reports/2019-04-02 14:59:54.411365.
```

## Report example
```bash
Orders to be generated: 2000
Red part: 15%
Green part: 60%
Blue part: 25%
Started at 02.04.2019 12:25:43.639
Finished at 02.04.2019 12:25:44.335
Total time is 695 ms

.:Method:.  =>  .:Time:.

'__writeZone' => 
	Max: 0.253 ms
	Average: 0.143133333333 ms
	Min: 0.045 ms
	Summary: 4.294
'__getRedZone' => 
	Max: 2.018 ms
	Average: 1.6187 ms
	Min: 1.428 ms
	Summary: 16.187
'__getGreenZone' => 
	Max: 3.965 ms
	Average: 3.0369 ms
	Min: 2.83 ms
	Summary: 30.369
'__getBlueZone' => 
	Max: 13.52 ms
	Average: 6.8415 ms
	Min: 5.526 ms
	Summary: 68.415
'__getEveryBatch' => 
	Max: 19.205 ms
	Average: 12.0788 ms
	Min: 10.512 ms
	Summary: 120.788
'generate' => 122.91 ms
'insertFromFile' => 531.62 ms

```

Inserts written to file:
```bash
--Red zone
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('Filled','Sell',14.83,'231977682659583',1145.0,'Green Peace','EUR/CAD','14.03.2019 15:14:09.352')
--Green zone
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',22.79,'248257772371579',641.0,'BitBon','AUD/JPY','18.03.2019 21:26:19.579')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',26.47,'115156283520147',685.0,'BitBon','USD/CHF','15.03.2019 13:22:27.147')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Buy',11.84,'469164181327984',950.0,'Home','EUR/USD','15.03.2019 14:13:04.984')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('To-provider','Buy',11.84,'469164181327984',950.0,'Home','EUR/USD','15.03.2019 14:13:38.943')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',13.41,'383304992612141',797.0,'Academy','AUD/EUR','13.03.2019 10:55:41.141')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',15.77,'756225622125277',604.0,'Academy','AUD/EUR','19.03.2019 04:34:37.277')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',23.89,'192897080864589',631.0,'Academy','AUD/EUR','18.03.2019 14:23:09.589')
--Blue zone
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',21.69,'268950791402069',722.0,'Academy','USD/CAD','17.03.2019 23:14:29.69')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('To-provider','Sell',21.69,'268950791402069',722.0,'Academy','USD/CAD','17.03.2019 23:14:48.160')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('Reject','Sell',21.69,'268950791402069',722.0,'Academy','USD/CAD','17.03.2019 23:16:47.387')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('New','Sell',23.11,'151001334432111',138.0,'Green Peace','EUR/CAD','18.03.2019 00:01:51.111')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('To-provider','Sell',23.11,'151001334432111',138.0,'Green Peace','EUR/CAD','18.03.2019 00:02:02.863')
INSERT INTO orders(status,direction,price,id,volume,tag,currencypair,orderdate) VALUES ('Filled','Sell',23.11,'151001334432111',138.0,'Green Peace','EUR/CAD','18.03.2019 00:03:53.905')
```

After all thease rows will be inserted into table in database which names are set in settings 