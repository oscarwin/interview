# new与malloc的区别以及实现方法

## new和malloc的内存分配在哪

分配在堆上。也有说new是分配在自由存储区而malloc分配在堆上，自由存储区可以是堆也可以不是，具体要看new内部的实现。操作系统在堆上维护一个空闲内存链表，当需要分配内存的时候，就查找这个表，找到一块内存大于所需内存的区域，分配内存并将剩余的内存空间返还到空闲链表上（如果有剩余的话）。

## new/delete和malloc/free的区别

**1. malloc和free是库函数，而new和delete是C++操作符；**

**2. new自己计算需要的空间大小，比如'int * a = new，malloc需要指定大小，例如'int * a = malloc(sizeof(int))'；**

**3. new在动态分配内存的时候可以初始化对象，调用其构造函数，delete在释放内存时调用对象的析构函数。而malloc只分配一段给定大小的内存，并返回该内存首地址指针，如果失败，返回NULL。**

**4. new是C++操作符，是关键字，而operate new是C++库函数**

**5. opeartor new /operator delete可以重载，而malloc不行**

 **6. new可以调用malloc来实现，但是malloc不能调用new来实现**

**7. 对于数据C++定义new[]专门进行动态数组分配，用delete[]进行销毁。new[]会一次分配内存，然后多次调用构造函数；delete[]会先多次调用析构函数，然后一次性释放。**
```
分配数组不同之处
int char* pa = new char[100];
int char* pb = malloc(sizeof(char) * 100);
```
**8. malloc能够直观地重新分配内存**

使用malloc分配的内存后，如果在使用过程中发现内存不足，可以使用realloc函数进行内存重新分配实现内存的扩充。realloc先判断当前的指针所指内存是否有足够的连续空间，如果有，原地扩大可分配的内存地址，并且返回原来的地址指针；如果空间不够，先按照新指定的大小分配空间，将原有数据从头到尾拷贝到新分配的内存区域，而后释放原来的内存区域。
new没有这样直观的配套设施来扩充内存。

## new和malloc内部实现的区别

### new
以下是从网上找来的一段关于new的代码，不知道和标准的实现是否有区别，但是原理应该是这样，足够来说明问题了：
```
void *__CRTDECL operator new(size_t size) _THROW1(_STD bad_alloc)  
      {       // try to allocate size bytes  
      void *p;  
      while ((p = malloc(size)) == 0)  
              if (_callnewh(size) == 0)  
              {       // report no memory  
                      _THROW_NCEE(_XSTD bad_alloc, );
              }  

     return (p);  
     } 
```

new: 可以理解成两步：
1. 调用operate new（）分配内存，如果内存不足失败，抛出异常；
2. 如果需要的话，在那段内存上初始化对象(赋值或者调用构造函数），这个应该是由编译器根据代码来控制的。

因此对于new和malloc检查是否正确分配的方法是不一样的

```
int *a  = (int *)malloc ( sizeof (int ));
if(NULL == a)
{
    ...
}
else 
{
    ...
}
从C语言走入C++阵营的新手可能会把这个习惯带入C++：

int * a = new int();
if(NULL == a)
{
    ...
}
else
{   
    ...
}
实际上这样做一点意义也没有，因为new根本不会返回NULL，而且程序能够执行到if语句已经说明内存分配成功了，如果失败早就抛异常了,后面的代码就不会执行了。正确的做法应该是使用异常机制：

try
{
    int *a = new int();
}
catch (std::bad_alloc& e)
{
    ...
}
```
为了照顾原来习惯的程序员，C++可以通过nothrow关键字来实现new不抛异常而是返回NULL。

```
int* p = new(std::nothrow) int;
```

### malloc

参考网上多篇文章，自己写了一个malloc，也没测过，如有错误欢迎指正。但是，用来说明malloc的原理的我想是没问题的。
```
#define malloc_addr 0x00000
#define malloc_size 0x22222

#ifndef NULL
#define NULL 0
#endif

void* managed_memory_start = NULL;  //堆区的起始地址
void* managed_memory_end = NULL;    //堆取的终止地址
int is_initialized = 0;

/*
 * 内存控制块，通过内存控制块将堆区的内存用双向链表连接起来管理
 */
typedef struct 
{
	unsigned int is_available;
	unsigned int current_block_size;
	unsigned int prev_block_size;
}mem_control_block;


void malloc_init(void)
{
	mem_control_block* tmp = NULL;
	managed_memory_start = (void*)malloc_addr;
	managed_memory_end = (void*)(malloc_addr + malloc_size);

	tmp = (mem_control_block*)managed_memory_start;
	tmp->is_available = 1;
	tmp->current_block_size = (managed_memory_end - managed_memory_start) - sizeof(mem_control_block);
	tmp->prev_block_size = 0;
	is_initialized = 1;
}

void* malloc(size_t size)
{
	//初始化，最开始链表只有一个节点
	if(!is_initialized)
	{
		malloc_init();
	}

	//保存内存地址游标
	void* current_location = NULL;
	//保存当前内存控制块的位置
	mem_control_block* current_location_mcb = NULL;
	//如果块太大，取下所需大小，剩余放回链表
	mem_control_block* leave_location_mcb = NULL;
	//定义一个用于返回的指针，返回的地址是控制块加上前面结构体的大小
	void* memory_location = NULL;

	//把游标指向堆的首地址
	current_location = managed_memory_start;

	while(current_location <= managed_memory_end)
	{
		current_location_mcb = (mem_control_block*)current_location;
		//判断该节点是否被空闲
		if(current_location_mcb->is_available)
		{
			//判断该空闲块大于需要，但是剩下的空间又不足以维持一个空闲块，就把整个块都分配了，为了维持链表的连续性
			//实际上也浪费不了多少内存，因为一个struct结构体很小
			if(current_location_mcb->current_block_size < size + 2 * sizeof(mem_control_block))
			{
				current_location_mcb->is_available = 0;
				break;
			}
			else //如果空闲块大于需要的，就把剩余的块放入leave_location_mcb节点了
			{
				unsigned int process_blocksize;

				//另当前块为被使用状态
				current_location_mcb->is_available = 0;
				process_blocksize = current_location_mcb->current_block_size;

				current_location_mcb->current_block_size = size + sizeof(mem_control_block);
				leave_location_mcb = (mem_control_block*)(current_location + process_blocksize);
				leave_location_mcb->is_available = 1;
				//当前块大小减去需要的内存减去一个控制块结构体就是剩余的大小
				leave_location_mcb->current_block_size =  process_blocksize - sizeof(mem_control_block) - size;
				//leaveo块的前一个块的大小就是要分配的大小
				leave_location_mcb->prev_block_size = size + sizeof(mem_control_block);
			}
		}
		//如果该块不空闲，则指针游标指向下一块的首地址
		current_location += current_location_mcb->current_block_size;
	}

	//如果空闲链表中已经没有合适的块就扩大堆区的范围
	if(!memory_location)
	{
		//申请取扩大堆取的内存
		if(sbrk(size + sizeof(mem_control_block)) != -1)
			return NULL;

		//如果空闲链表中没有合适的块，那么必然是遍历了整个链表，此时的current_location_mcb指向原来空闲链表的最后一个块
		//将该块的大小保存下来，就是马上要分配块的前一个块的大小了
		unsigned int prev_size = current_location_mcb->current_block_size;

		//之前的循环会使得current_location指向最后一个块末尾的下一个地址
		current_location_mcb = (mem_control_block*)current_location;
		current_location_mcb->current_block_size = size + sizeof(mem_control_block);
		current_location_mcb->prev_block_size = prev_size;
	}

	memory_location = current_location + sizeof(mem_control_block);
	return memory_location;
}
```

系统为堆区保存了两个指针一个指向堆的首地址，一个指向堆的尾地址(我猜想这两个指针是不是就是有vm_area_struct里的两个指针维护的，源码还没看到只是猜测)。系统通过结构体mem_control_block将整个堆区分成一个个块，每个块都已这样一个结构体开头，结构体里维护了块的大小。malloc分配内存的时候，从第一个块开始遍历，如果找到了块已经被使用，那么就找下一个块，如果找到的块比需要的小继续找下一个块，直到找到比我需要大于等于的块，然后将该块mem_control_block中的标志位设置为被使用了，如果块有剩余的就将剩余的空间添加一个mem_control_block变成一个新块。如果遍历了整个堆空间都没有找到合适的块，那么就调用sbrk函数扩大堆的范围。

>brk()  and  sbrk() change the location of the **program break**, which defines the end of the process's data segment (i.e., the program break is the first location after the end of the uninitialized data segment).  Increasing the program break has the effect of allocating memory to the process; decreasing the break deallocates memory.

>**brk() sets the end of the data segment to the value specified by addr**, when that value is reasonable, the system has enough memory, and the process does not exceed its maxi‐mum data size (see setrlimit(2)).

>**sbrk()increments the program's data space by increment bytes**.  Calling sbrk() with an increment of 0 can be used to find the current location of the program break.

上面这段摘自Linux手册，brk函数和sbrk都是扩大堆区(program break就是堆，因为文中说了program break就是bss后的第一个位置)尾地址的。只不过brk通过指定一个地址，而sbrk通过追加一个大小。

通过上面的代码我们可以直到当我们调用malloc分配n个字节的空间时，实际上占用了n + sizeof(mem_control_block)个字节的空间。但是返回的地址是紧跟结构体mem_control_block后面的第一个地址。那么相信聪明的你已经猜到了free是如何释放内存的了。没错，就是把指针往回倒个sizeof(mem_control_block)的距离，然后设置标志位为可用。为了减少内存碎片，会取查找前面一个块和后面一个块，如果有空闲块就合并为一个。

>给free()中的参数就可以完成释放工作！这里要追踪到malloc()的申请问题了。申请的时候实际上占用的内存要比申请的大。因为超出的空间是用来记录对这块内存的管理信息。先看一下在《UNIX环境高级编程》中第七章的一段话：

>大多数实现所分配的存储空间比所要求的要稍大一些，额外的空间用来记录管理信息——分配块的长度，指向下一个分配块的指针等等。这就意味着如果写过一个已分配区的尾端，则会改写后一块的管理信息。这种类型的错误是灾难性的，但是因为这种错误不会很快就暴露出来，所以也就很难发现。将指向分配块的指针向后移动也可能会改写本块的管理信息。


#参考：

[浅谈 C++ 中的 new/delete](http://blog.csdn.net/hazir/article/details/21413833)

[文章1](http://www.linuxidc.com/Linux/2016-01/127591.htm)

[文章2](http://www.cnblogs.com/ThuremansC/p/6606622.html)

[文章3](http://www.cnblogs.com/huhuuu/archive/2013/11/19/3432371.html)

[如何实现一个malloc](http://www.cnblogs.com/amanlikethis/p/3765908.html)