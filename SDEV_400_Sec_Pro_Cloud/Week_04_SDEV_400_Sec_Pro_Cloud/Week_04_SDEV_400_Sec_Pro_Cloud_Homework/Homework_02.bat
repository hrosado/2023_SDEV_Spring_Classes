ECHO 'Hello Python'
aws dynamodb batch-write-item --request-items file://courses.json --return-consumed-capacity INDEXES --return-item-collection-metrics SIZE