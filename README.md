# DreamStorm

A Crawler Library
Support : 
- multi-thread
- tor

## Example

```python
from DreamStorm.Connector import Connector

def example_callback(page,headers):
    print "server : " + headers["server"]

C = Connector(5) # how many threads to use
C.put(["https://oalieno.github.io","http://www.nctu.edu.tw"])
C.run(example_callback)
```
