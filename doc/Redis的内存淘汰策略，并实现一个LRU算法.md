## Redis 的内存淘汰策略，并实现一个 LRU 算法

### 什么是 LRU 算法
LRU 算法是最近最少使用的意思，最近最少使用这个解释可能不太好理解，换句话说就是：选择上次使用的时间距离现在时间差最大的那个，将其淘汰。

LRU 算法似乎离我们很远，其实很近。LRU 也是操作系统内存淘汰算法之一，对于输入框的搜索记录也可以采用这种方式进行淘汰。

### Redis 的6种内存淘汰策略

Redis 可以在配置文件中配置 maxmemory 选项来限制 redis 使用的最大内存，也可以通过 CONFIG SET 命令进行配置，默认值是 3GB。比如要设定最大使用内存为 100mb，可以使用如下配置：

```
maxmemory 100mb
```

当 redis 使用的内存到达最大内存限制时，如果配置了内存淘汰策略，会根据相应的策略淘汰旧的数据，从而释放出空间供新的数据使用。

- noeviction：不删除策略，达到最大内存限制时, 如果需要更多内存, 直接返回错误信息。

- allkeys-lru：对所有的 key 使用 LRU(less recently used, 最近最少使用) 算法。

- volatile-lru：只对设置了过期时间的 key 使用 LRU 算法。

- allkeys-random：对所有的 key，随机选择一部分进行删除。

- volatile-random: 只对设置了过期时间的 key，随机选择一部分进行删除。

- volatile-ttl：对于设置了过期时间的 key，选择剩余时间(TTL)短的优先淘汰。

淘汰策略需要根据业务场景进行合理选择，不过一般有如下经验可以参考：

- 如果你的业务中有些数据访问频繁，有些数据访问较少，那么可以选择 allkeys-lru 策略。如果你不知道选择哪种策略，那么也选这种策略，至少不会太差。

- 如果你的业务中所有的 key 都会循环访问，那么可以选择 allkeys-random。

- 如果你想指引 redis 选择哪些 key 进行淘汰，可以选择 volatile-ttl 策略。把想淘汰的数据的 TTL 设置的小一些，把不想淘汰的数据的 TTL 设置的大一些。

如果 redis 中同时保存了缓存数据和永久存储的数据，那么 volatile-lru 和 volatile-random 策略就非常有用了。不过更好的方法是将这两种数据分两个实例进行存储。

为每个 key 设置过期时间也会耗费内存空间，而 allkeys-lru 策略淘汰时不需要 key 设置了过期时间，因此对内存的使用效率更高。

实际上 redis 采用的并不是完整的 LRU 算法，而是 LRU 的近似算法。redis 选择了一部分 key 进行 LRU 淘汰，因为维护所有的 key 需要耗费大量的内存。在 redis-3.0 以后可以选择一批对象进行淘汰，这使得该算法可以更加趋近于完整的 LRU 算法。

### 实现 LRU 算法

LRU 算法一般通过一个链表和一个 map 来实现，链表维护数据的位置，每次访问一个数据就将其移动到链表的头部。链表的查询复杂度是 O(N)，为了加快查询速度使用 map 再存一个映射关系可以将查询的时间复杂度也降到 O(1)。

1 将所有的数据放入链表。

2 新插入的数据，插入在链表的头部。

3 访问一个数据，访问完后，将其移动到链表的头部。

4 当需要淘汰数据时，淘汰链表尾部数据就行，这个数据就是最近最少使用的数据。

5 由于链表的查询复杂度是 O(N)，为了减小查询的复杂度使用一个 map 存储数据再链表上的位置，map 中的 key 是要访问的数据的 key，map 中的 value 是指向要访问的数据链表节点的指针。

```cpp
#include <string>
#include <map>

// 链表节点的结构体
typedef struct NODE
{
    std::string key;
    void* value;
    struct NODE* pre;
    struct NODE* next;
}node;

// 链表结构体
typedef struct LIST
{
    node* head;
    node* tail;
    unsigned int count;
}list;

// 通过链表和map实现一个LinkedHashmap结构，用来实现LRU算法
class CLinkedHashmap
{
public:
    CLinkedHashmap();
    ~CLinkedHashmap();
    void Insert(const std::string& strKey, void* value);
    void* Find(const std::string& strKey);
    void Delete();

public:
    list* m_lru_list;
    std::map<std::string, node*> m_lru_map;
};

CLinkedHashmap::CLinkedHashmap()
{
    m_lru_list = new list;
    m_lru_list->head = NULL;
    m_lru_list->tail = NULL;
    m_lru_list->count = 0;
}

CLinkedHashmap::~CLinkedHashmap()
{
    delete m_lru_list;
    m_lru_list = NULL;
}

// 插入方法，向链表中插入一个新的节点，且插入到链表的头部
void CLinkedHashmap::Insert(const std::string& strKey, void* value)
{
    node* pNode = new node;
    pNode->key = strKey;
    pNode->value = value;

    // 如果链表中没有节点
    if (m_lru_list->count == 0)
    {
        pNode->pre = pNode->next = NULL;
        m_lru_list->head = m_lru_list->tail = pNode;
    }
    else
    {
        pNode->pre = NULL;
        pNode->next = m_lru_list->head;
        m_lru_list->head->pre = pNode;
        m_lru_list->head = pNode;
    }
    m_lru_map[strKey] = pNode;
    m_lru_list->count++;
}

// 查询方法，返回该数据的值，并且将该节点移动到链表的头节点上
void* CLinkedHashmap::Find(const std::string& strKey)
{
    if (m_lru_map.find(strKey) == m_lru_map.end())
    {
        return NULL;
    }

    node* pNode = m_lru_map[strKey];

    // 如果该节点已经是头节点，则不用移动位置。如果不是头节点则移动到头节点。
    if (pNode->pre)
    {
        pNode->pre->next = pNode->next;
        // 如果不是尾节点，则将其上一个节点的next指向该节点的下一个节点
        // 如果是尾节点，则将链表的尾节点指向该节点的上一个节点
        if (pNode->next)
        {
            pNode->next->pre = pNode->pre;
        }
        else
        {
            m_lru_list->tail = pNode->pre;
        }
        pNode->pre = NULL;
        pNode->next = m_lru_list->head;
        m_lru_list->head->pre = pNode;
        m_lru_list->head = pNode;
    }

    return pNode->value;
}

// 淘汰链表的最后一个元素
void CLinkedHashmap::Delete()
{
    if (m_lru_list->count == 0)
    {
        return;
    }

    // 从map中清除该元素
    std::map<std::string, node*>::iterator it;
    it = m_lru_map.find(m_lru_list->tail->key);
    m_lru_map.erase(it);

    // 如果最后只剩下一个元素，直接删除
    // 如果还有其他元素，需要将该节点的上一个节点指向NULL，将链表的尾节点指针指向该节点的上一个节点
    if (m_lru_list->count == 1)
    {
        delete m_lru_list->tail;
        m_lru_list->tail = NULL;
        m_lru_list->head = NULL;
    }
    else
    {
        node* pNode = m_lru_list->tail;
        m_lru_list->tail = m_lru_list->tail->pre;
        m_lru_list->tail->next = NULL;
        delete pNode;
        pNode = NULL;
    }

    m_lru_list->count--;
}
```

### 参考

[Using Redis as an LRU cache](https://redis.io/topics/lru-cache)