题目：已知sqrt(2)约等于1.414，要求不用数学库，求sqrt(2)精确到小数点后10位

思路：二分法

代码：/src/sqrt2.py

```python
def sqrt2():
    begin = 1.4
    end = 1.5
    mid = (begin + end) / 2

    stop = 0.0000000001

    while end - begin > stop:
        if mid * mid > 2:
            end = mid
        else:
            begin = mid
        
        mid = (begin + end) / 2
    
    return mid

if __name__ == "__main__":
    print(sqrt2())
```