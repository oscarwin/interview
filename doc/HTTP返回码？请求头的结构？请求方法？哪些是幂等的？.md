# HTTP 返回码？请求头的结构？请求方法？哪些是幂等的？

### HTTP 返回码

*2xx系列：请求成功*

- 200：成功
- 201：服务器已经创建了文档
- 202：请求已接受，但处理尚未完成
- 204：No Content，请求处理成功但没有资源可返回。在客户端向服务端发送信息，而服务器不需要返回信息时使用。

*3xx系列：重定向*

- 301：永久重定向
- 302：临时重定向
- 303：See Other，查看其它。类似于302，不同之处在于，303表示客户端应该使用GET方法来获取这个新信息。
- 304：未修改。提示客户端原来缓存中的信息还可以用。
- 305：Use Proxy 使用代理。客户请求的文档应该通过Location头所指明的代理服务器提取（HTTP 1.1新）。

*4xx系列：客户端错误*

- 400：错误请求。请求格式错误。
- 401：未授权。提示客户端进行账户密码登录。
- 402：需要付款。
- 403：禁止访问。通常因为服务器上文件权限的问题而禁止访问。
- 404：文件未找到。
- 405：方法不允许。请求方法（GET,POST,PUT,DELETE,TRACE等）对指定的资源不可用。
- 406：不可接受。指定的资源已经找到，但它的MIME类型和客户在Accpet头中所指定的不兼容，客户端浏览器不接受所请求页面的 MIME 类型。
- 407：需要代理认证。要求进行代理身份验证，类似于401，表示客户必须先经过代理服务器的授权。
- 408：请求超时。在服务器许可的时间内，客户一直没有发起任何请求。
- 409：冲突。通常和 PUT 请求有关，由于请求和资源的当前状态相冲突，因此请求不能成功。

*5xx系列：服务端错误*

- 500：服务器内部错误。
- 501：没有实现。服务器没有实现请求所需要的功能。
- 502：CGI 应用超时。
- 503：Bad Gateway 错误的网关。服务器作为网关或者代理时，为了完成请求访问下一个服务器，但该服务器返回了非法的应答。亦说Web 服务器用作网关或代理服务器时收到了无效响应。
- 504：Gateway Timeout 网关超时。服务器作为网关或者代理时，不能及时获取远程服务器的响应。
- 505：版本不支持。服务器不支持请求中所指明的 HTTP 版本。
- 507：存储不足。

### HTTP 的请求方法与幂等性

- GET：请求显示指定的资源，一般只用来读取数据。GET 方法是幂等的。
- HEAD：HEAD方法与GET方法一样，都是向服务器发出指定资源的请求。但是，服务器在响应HEAD请求时不会回传资源的内容部分，即响应主体。这样，我们可以不传输全部内容的情况下，就可以获取服务器的响应头信息。HEAD方法常被用于客户端查看服务器的性能。
- POST：请求向服务器指定的资源提交数据，如表单提交、文件上传等。POST方法是非幂等的方法，因为这个请求可能会创建新的资源或/和修改现有资源。
- PUT：客户端可以将指定资源的最新数据传送给服务器取代指定的资源的内容。PUT 方法是幂等的。
- DELETE：请求删除所请求的 URL。DELETE 是幂等的。
- CONNECT：是 HTTP 1.1 预留的，能够将连接改为管道方式的代理服务器。通常用于SSL加密服务器的链接与非加密的HTTP代理服务器的通信。
- OPTIONS：OPTIONS 请求与 HEAD 类似，一般也是用于客户端查看服务器的性能。
- TRACE：回显服务器收到的请求，用于测试或诊断。回显数据所以是幂等的。

### HTTP 请求头的结构

第一行是请求行，标明了请求的方法，请求的 URL 和 HTTP 的版本。然后是请求头，请求头标识了host，User-Agent等信息。之后空一行，空行后是具体的请求参数信息。GET 的参数直接在 URL 里了，因此这一块就没有数据了。POST 的请求参数就是放在这里。