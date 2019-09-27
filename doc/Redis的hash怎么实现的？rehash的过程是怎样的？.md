## Redis 的 hash 怎么实现的？rehash 的过程是怎样的？

Redis 的 hash 结构采用压缩列表或 hashmap 来实现，当 hash 结构中的元素较少时采用压缩链表，当元素较多时会从压缩链表转成 hashmap。

Redis 的 hashmap 采用拉链的方式来解决地址冲突。

Redis 的 hashmap 需要扩缩容时，通过渐进的方式进行 rehash。redis 为一个 hashmap 会维护两个 hash 结构，hash[0] 和 hash[1]。

1 一般情况下只使用 hash[0] 进行查询和存储，rehash 时再为 hash[1] 分配空间；

2 hash 字典中维护了一个索引计数器变量 rehashidx，一般状态下该变量为-1，将该变量置0表示 rehash 开始；

3 在 rehash 期间每次操作这个 key 执行添加、删除、查找或者更新时，除了完成指定的任务，还会顺带将 hash[0] 中在索引 rehashidx 上的所有元素迁移一个元素到 hash[1] 中，并将 rehashidx 的值加1;

4 rehash 迁移期间，写操作全部写到 hash[1] 中，读操作先读 hash[0]，如果读到数据直接返回，如果读不到数据再读一次 hash[1]；

5 hash[0] 上的数据全部迁移到 hash[1] 中后，释放 hash[0] 的内存，将 hash[0] 指向 hash[1] 的位置，将 hash[1] 指向 null，最后将 rehashidx 的值置为-1表示整个过程结束;