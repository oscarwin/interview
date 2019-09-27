# static 关键词的作用

static 是 C 和 C++ 的关键词，static 在 C++ 中比在 C 中有着更丰富的用法。

## 1 static 修饰局部变量

static 修饰局部变量时，使得被修饰的变量成为静态变量，存储在静态区。存储在静态区的数据生命周期与程序相同，在main函数之前初始化，在程序退出时销毁。（无论是局部静态还是全局静态）

局部静态变量使得该变量在退出函数后，不会被销毁，因此再次调用该函数时，该变量的值与上次退出函数时值相同。值得注意的是，生命周期并不代表其可以一直被访问，因为变量的访问还受到其作用域的限制。

```
void function()
{
	/*实际上nCount的初始化不是在函数体第一次执行时完成，而是在编译期其值就已经被
	   确定，在main函数之前就完成了初始化，所以局部静态变量只会初始化一次*/
	static int nCount(0);    
	std::cout << "call function " << ++nCount << " times" << endl;
}

int main()
{
	for (int i = 0; i < 5; ++i) 
	{
		function();
	}
	return 0;
}
```

输出结果是：
```
call function 1 times
call function 2 times
call function 3 times
call function 4 times
call function 5 times
```

## 2 static 修饰全局变量
全局变量本来就存储在静态区，因此static并不能改变其存储位置。但是，static限制了其链接属性。被static修饰的全局变量只能被该包含该定义的文件访问。

在头文件a.h中定义一个全局变量
```
//头文件a.h
#pragma once

int a = 1;
```

```
//实现文件a.cpp,包含头文件a.h
#include "a.h"
#include "b.h"
#include <iostream>

using namespace std;

int main()
{
	fun();
	return 0;
}
```

```
//实现文件b.cpp，包含头文件a.h
#include "a.h"
#include <iostream>

using namespace std;

void fun()
{
	cout << a << endl;
}
```
编译出现**重定义错误**，因为头文件a被包含两次，在a.cpp和b.cpp分别被定义了一次。
![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwNjA3MjAzNDEyMDA5)

要解决这样的冲突怎么办？两种解决办法。
1. 将a定义为静态的全局变量。

```
//头文件a.h
#pragma once

static int a = 1;

```

```
//实现文件a.cpp,包含头文件a.h
#include "a.h"
#include "b.h"
#include <iostream>

int main()
{
	fun();
	std::cout << a << std::endl;
	return 0;
}
```

```
//实现文件b.cpp，包含头文件a.h
#include "a.h"
#include <iostream>

void fun()
{
	a = 2;
	std::cout << a << std::endl;
}
```
输出结果：
![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwNjA3MjA0MjAzNTQz)
从输出的结果可以发现，在文件b中修改全局变量a，并没有使文件a中的变量a发生变化。原因是，静态全局变量a在文件在a.cpp和b.cpp分别进行了定义。使得全局变量可以同名。

2. 使用extern，将a声明为extern类型的变量。

## 3 static 修饰函数
static修饰函数使得函数只能在包含该函数定义的文件中被调用。

在头文件b.h中声明静态函数fun()，在文件b.cpp中定义静态函数fun()，编译器会报错，指明b.h中的fun函数未定义。
对于静态函数，声明和定义需要放在同一个文件夹中。

如果将static函数定义在头文件中，则每一个包含该头文件的文件都实现了一个fun函数。因此static实现了不同文件中定义同名的函数，而不发生冲突。

在多人协同工作的项目中，为了避免出现同名的函数冲突，可以将函数定义为static，从而避免冲突的发生。

## static 在 C++ 中的作用

在C++中static不光具备C中所有的作用，而且对于静态成员变量和静态成员函数。所有的对象都只维持同一个实例。
因此，采用static可以实现不同对象之间数据共享。