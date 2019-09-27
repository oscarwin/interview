# Kafka 中 publisher, subscriber, topic, broker, partition，producer, consumer, consumer group 分别指什么？

Broker：是 kafka 服务器进程的代名词，可以分布在同一台机器上，也可以分布在多台机器上；

Topic：是发布和订阅的对象，是用来承载消息的逻辑容器；

Partition：分区，一个 Topic 可以有多个分区，用来承载更大的 QPS；

Producer：生产者，也就是发布者(publisher)，向 Topic 写入数据消息；

Consumer：消费者，也就是订阅者(subscriber)，订阅一个 Topic，消费其中的消息；

Consumer group：消费者组，一个消费者组里可以有多个消费者，这多个消费者共同消费一份消息，这些消费者同时消费多个分区提高吞吐。

Replica：副本，kafka 中同一条消息能够被拷贝到多个地方提供冗余，副本分为领导者副本和追随者副本。