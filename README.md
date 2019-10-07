# Exchange orders history generator
It generates orders according to configurations. 
Here is RabbitMq publishing and consuming service.
Rows are encoded to protocol buffer format first, and then send to rmq queue.
After consuming messages data is inserted into table in database.
Objects are generating, sending, inserting by batches, what size you set in configurations.
Customize objects that you generate.

Clone url:

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
Create database first.
You can find sql script in files/sql/ to create table
Execute it in your db. Or just set correct dbname in configs, and table will be created.


Then set you hosts and passwords in defaults.json

After that just run python command.


## Start app

```
$ python launcher.py -c --loggermode=info --configs defaults.json
```

--loggermode is a level of output logs. Can be: trace, debug, info, warning, error, critical, fatal.

-f file writing logs.

-c console writing logs.

--configs is a path to your config file.

All options are not required.
By default is info, console and file writing, defaults.json


---
## See result
```bash
$ python launcher.py --loggermode=INFO 
[LOGGER]: Started with default settings.
[LOGGER]: Logger mode is now set to INFO.
[INFO]: Initializing application...
[INFO]: Loading configs from files/defaults.json.
[INFO]: Configurations for generating loaded.
[INFO]: Configurations for database usage loaded.
[INFO]: Configurations for messaging loaded.
[INFO]: Table 'orders' exists.
[INFO]: All records from table 'orders' have been deleted.
[INFO]: Initializing completed.
[INFO]: Generation started...
[INFO]: Sending records to RabbitMQ started.
[INFO]: Batch 0.
[INFO]: Batch 1.
[INFO]: Batch 2.
[INFO]: Batch 3.
[INFO]: Batch 4.
[INFO]: Batch 5.
[INFO]: Batch 6.
[INFO]: Batch 7.
[INFO]: Batch 8.
[INFO]: Batch 9.
[INFO]: Generation finished.
[INFO]: Orders created: 1000.
[INFO]: Sending records to RabbitMQ stopped.
[INFO]: Start consuming records from RabbitMQ.
[INFO]: Consuming started.
[INFO]: Consuming is finished. Messages count = 2465
[INFO]: Rows are inserted into table. There are 2431 records
[INFO]: Report is made in file files/reports/Mon Oct  7 22:58:49 2019.
```

## Report example
```bash
Checkpoint number: 1

After start: 0.00426 s
Red zone: objects = 0, inserts = 0
Green zone: objects = 0, inserts = 0
Blue zone: objects = 0, inserts = 0
Generated objects count: 0
Rows in csv written to file: 0
Send messages count: 0
Consumed messages count: 0
Rows inserted: 0


Checkpoint number: 2

After start: 0.05888 s
Red zone: objects = 150, inserts = 236
Green zone: objects = 600, inserts = 1800
Blue zone: objects = 250, inserts = 396
Generated objects count: 1000
Rows in csv written to file: 0
Send messages count: 2465
Consumed messages count: 340
Rows inserted: 286


Checkpoint number: 3

After start: 0.10254 s
Red zone: objects = 150, inserts = 236
Green zone: objects = 600, inserts = 1800
Blue zone: objects = 250, inserts = 396
Generated objects count: 1000
Rows in csv written to file: 0
Send messages count: 2465
Consumed messages count: 1978
Rows inserted: 1892

Orders to be generated: 1000
Red part: 15%
Green part: 60%
Blue part: 25%
Started at 07.10.2019 19:58:02.943
Finished at 07.10.2019 19:58:05.321
Total time is 3.7766 s

.:Method:.  =>  .:Time:.

'insertFromFile' => [0.16] ms
'sendObjects' => 
	Max: 241.35 ms
	Average: 107.762 ms
	Min: 31.42 ms
	Summary: 3232.85 ms
'__getBlueZone' => 
	Max: 56.34 ms
	Average: 51.909 ms
	Min: 48.54 ms
	Summary: 519.09 ms
'__getRedZone' => 
	Max: 52.93 ms
	Average: 36.708 ms
	Min: 30.02 ms
	Summary: 367.08 ms
'insertConsumedObjects' => 
	Max: 434.86 ms
	Average: 184.379 ms
	Min: 0.07 ms
	Summary: 5531.36 ms
'__getGreenZone' => 
	Max: 268.97 ms
	Average: 235.444 ms
	Min: 199.36 ms
	Summary: 2354.44 ms
'__getEveryBatch' => 
	Max: 689.94 ms
	Average: 654.969 ms
	Min: 632.16 ms
	Summary: 6549.69 ms
'generate' => [2952.22] ms

Generated objects count: 1000
Rows in csv written to file: 0
Send messages count: 2465
Consumed messages count: 2465
Rows inserted: 2432

Results of select query

Total count: 1000  100%
Green zone count: 600  60.0%
Red zone count: 150  15.0%
Blue zone count: 250  25.0%

```