SELECT * FROM system.clusters;


CREATE TABLE station_metrics_kafka
(
    timestamp DateTime,
    station_id UInt32,
    metric_name String,
    value Float64
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = '103.175.198.215:9092',  -- List of Kafka brokers
    kafka_topic_list = 'station_metrics',                        -- Kafka topic name
    kafka_group_name = 'station_metrics_group',                  -- Kafka consumer group
    kafka_format = 'JSONEachRow',                                -- Format of the Kafka messages
    kafka_num_consumers = 4,                                     -- Number of Kafka consumers
    kafka_max_block_size = 1000;                                 -- Maximum number of messages in one batch

CREATE TABLE station_metrics_distributed
AS station_metrics_kafka
ENGINE = Distributed(
    'cluster_2S_1R',   -- Cluster name defined in <remote_servers>
    'default',                 -- Database name
    'station_metrics_kafka',         -- Table name on shards
    station_id                  -- sharding key
);

CREATE MATERIALIZED VIEW station_metrics_mv
TO station_metrics_distributed
AS
SELECT
    timestamp,
    station_id,
    metric_name,
    value
FROM station_metrics_kafka;


SHOW CREATE TABLE station_metrics_distributed;

SELECT * FROM system.kafka_consumers;

SELECT
    station_id,
    count(*)
FROM station_metrics_distributed
GROUP BY station_id;

SELECT
    station_id,
    count(*)
FROM station_metrics_distributed
GROUP BY station_id;


SELECT * FROM station_metrics_distributed LIMIT 10;

SYSTEM RESTART CONSUMERS station_metrics_kafka;


kafka-topics --describe --topic station_metrics --bootstrap-server 103.175.198.215:9092

kafka-topics --alter --topic station_metrics --partitions 4 --bootstrap-server 103.175.198.215:9092


kafka-broker-api-versions --bootstrap-server 103.175.198.215:9092

kafka-consumer-groups --bootstrap-server 103.175.198.215:9092 --group station_metrics_group --describe
