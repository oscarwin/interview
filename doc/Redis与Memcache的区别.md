## Redis 与 Memcache 的区别

1. 是否支持持久化

Memecache 不支持持久化，掉电后数据不能恢复到内存中。

Redis支持持久化，有 RDB 和 AOF 两种持久化方式，掉电后Redis会自动加载磁盘中的文件到内存中。

2. 数据结构

Memcache 只支持 string 类型的数据格式。

Redis 除了string 之外还有 list，hash，set，sorted set, bitmap, hyperloglog, geo 等。

3. 网络库

Memcache 使用 libevent 作为网络库来处理文件事件。

Redis 封装了 socket 函数，单独实现了 reactor 模式的文件事件。

libevent 是多线程的，因此可以充分利用多核 CPU 的性能。而 redis 是单线程的，不能利用到 CPU 多核的性能。redis 的作者之所以设计成单线程模式，是希望采用多实例的方式来提高性能。因为现代系统基本都是分布式的，通过多实例的方式可以水平扩展。