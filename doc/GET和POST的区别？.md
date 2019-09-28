## GET 和 POST 的区别？

1 get重点在从服务器上获取资源，post重点在向服务器发送数据。如果RESTful风格的接口，对于同一个url而言，get和post一个进行读操作，一个进行写操作。

2 get传输数据是通过URL请求，以field（字段）= value的形式，置于URL后，并用"?"连接，多个请求数据间用"&"连接，如http://127.0.0.1/Test/login.action?name=admin&password=admin。
post传输数据通过Http的post机制，将字段与对应值封存在请求实体中发送给服务器，可以使用纯文本，也可以使用json等格式。

3 get传输的数据量小，因为受URL长度限制，但效率较高。post可以传输大量数据，所以上传文件时只能用Post方式。

4 get请求中，URL将参数完全暴露给用户。而post请求将参数放在请求头中，相对而言更加安全一些。

5 对于跨域的问题。jsonp可以解决get请求跨域的问题，而post请求不能通过jsonp来解决跨域。CORS(Cross-origin resource sharing 跨域资源共享)可以同时解决get和post的跨域问题。