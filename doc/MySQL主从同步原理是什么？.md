1) 从服务器上有一个 IO 线程，IO 线程和主服务器连接，IO 线程定时请求主服务器上指定位置以后的 binlog 日志内容（再开始建立主从的时候是从告诉主从哪里开始复制，建立连接后是主发生更新后主动发送给从）；

2) 主服务器收到从服务 IO 线程的请求后，负责复制的 IO 线程根据请求信息复制指定位置以后的 binlog 日志发送给从服务器的 IO 线程。除了日志内容外，主服务器还会将 binlog 日志的名称和同步的位置也发送给从服务器 IO 线程；

3) 从服务器 IO 线程收到主服务器发来的日志文件后，将其依次追加到本机的 relay-log 日志的末端，并将读取到的主服务器的 binlog 日志名称和同步的位置记录到 master-info 中；

4) 从服务器的 sql 线程检测到 relay-log 日志发生变动后，解析新增的 relay-log 日志并在本机执行相应的 sql 语句，达到和主机相同的状态。