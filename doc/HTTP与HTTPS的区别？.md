## HTTP 与 HTTPS 的区别？

HTTP 是不安全的，HTTPS 是安全的。HTTPS 实际上就是 HTTP 加上 SSL 来实现安全的传输协议。

HTTP 不安全性表现在：

- HTTP 采用明文传输，信息可能被窃取；

- HTTP 不验证通信方的身份，因此有可能遭遇伪装。服务端可能是伪装的，客户端也可能是伪装的；

- HTTP 无法证明报文的完整性，所以有可能遭到篡改；

因此，HTTPS = HTTP + 加密 + 认证 + 完整性保护