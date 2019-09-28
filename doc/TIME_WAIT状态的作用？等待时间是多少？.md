## TIME_WAIT 状态的作用？等待时间是多少？

TIME_WAIT 出现的主动发起的一端，TIME_WAIT 的作用是为了防止最后一个 ACK 包丢失，留下充分的时间让对端进行重传。因此 TIME_WAIT 等待的时长是 2TTL。TTL 是一个数据包在网络中停留的最长时间。