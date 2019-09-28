# Redis 中 save 和 bgsave 的区别？

save 直接调用 rdbsave，阻塞 redis 的主进程，知道保存为止。阻塞期间不能处理客户端请求。

bgsave 则 fork 出一个子进程，子进程调用 rdbsave，并在保存完成之后向主进程发送信号，通知保存已完成。 Redis 服务器在BGSAVE 执行期间仍然可以继续处理客户端的请求。