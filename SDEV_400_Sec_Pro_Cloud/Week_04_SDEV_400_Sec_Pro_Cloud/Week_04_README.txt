Week_04_SDEV400 README

DynamoDB Commands CLI:
https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html#cli-aws-dynamodb
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html


DISCUSSION: See word file

Weekly Learning Objectives
[] - Compare SQL and No SQL database technology concepts and components.
[] - Write Python code to populate NO SQL databases.
[] - Create an application to search NO SQL database


For this week you should complete the following tasks:
Content-Related:
[o] - Read "DynamoDB Core Components"
[o] - Read "DynamoDB API"
[o] - Read "Naming Rules and Data Types"
[] - Read "Read Consistency"
[] - Read "Read Write Capacity"
[] - Read "Partitions and Data Distribution"
[] - Read, analyze and experiment with the "Using DynamoDB" PDF document
[] - Download and experiment with the Week4-DynamoDB-PythonCode examplles.

Assignments Related:
[] - Post any questions you may have in the "Ask the Professor" Discussion area.
[] - Complete and Submit Homework 2- Using DynamoDB

DynamoDB Core Components
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html

DynamoDB API
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.API.html

Naming Rules and Data Types
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html

Read Consistency
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html

Read Write Capacity
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html

Partitions and Data Distribution
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html

PDF - UsingDynamoDB
https://leocontent.umgc.edu/content/dam/permalink/acf51aab-8ca2-4a1c-850f-5cfd65937af6.html

ZIP - Week4-DynamoDB-PythonCode
https://leocontent.umgc.edu/content/dam/permalink/7bade0ee-b425-4667-8846-08d125bffd4f.html


Python Textbook
"A Byte of Python" from:

https://python.swaroopch.com/

https://github.com/swaroopch/byte-of-python/releases/tag/v239134197cc453397b0540fa051392af6b47f9f3


DynamoBD Commands list:
Available Commands¶
batch-execute-statement
batch-get-item
batch-write-item
create-backup
create-global-table
create-table
delete-backup
delete-item
delete-table
describe-backup
describe-continuous-backups
describe-contributor-insights
describe-endpoints
describe-export
describe-global-table
describe-global-table-settings
describe-import
describe-kinesis-streaming-destination
describe-limits
describe-table
describe-table-replica-auto-scaling
describe-time-to-live
disable-kinesis-streaming-destination
enable-kinesis-streaming-destination
execute-statement
execute-transaction
export-table-to-point-in-time
get-item
import-table
list-backups
list-contributor-insights
list-exports
list-global-tables
list-imports
list-tables
list-tags-of-resource
put-item
query
restore-table-from-backup
restore-table-to-point-in-time
scan
tag-resource
transact-get-items
transact-write-items
untag-resource
update-continuous-backups
update-contributor-insights
update-global-table
update-global-table-settings
update-item
update-table
update-table-replica-auto-scaling
update-time-to-live
wait


scan() 
ADD ITEMS TO TABLE:
aws dynamodb batch-write-item \ 
    --request-items file://inputs.json \
    --return-consumed-capacity INDEXES \
    --return-item-collection-metrics SIZE
Format of the inputs.json file would be something like (2 example records) this to use the CLI Import
{ 
    "Sensors": [
        {
            "PutRequest": {
                "Item": {
                    "Sensor": {"S": "Sensor1"},
                    "SensorDescription": {"S": "Sensor1 Description"},
                    "ImageFile": {"S": "/Sensors/images/acoustic1-elementarray.jpg"},
                    "Locations": {"SS": ["Tampa FL", "Destin FL", "Orlando FL"]}
                }
            }
        },
        {
            "PutRequest": {
                "Item": {
                    "Sensor": {"S": "Sensor2"},
                    "SensorDescription": {"S": "Sensor2 Description"},
                    "ImageFile": {"S": "/Sensors/images/acoustic2-elementarray.jpg"},
                    "SampleRate": {"N": "2002"},
                    "SensorType": {"S": "Temp"},
                    "Locations": {"SS": ["Kansas City MO", "St Louis MO"]}
                }
            }
        } 
   ]
}

