# DreamStorm

A Crawler Library

Support : 
- multi-thread
- tor

## Dependency

### tor

`apt-get install tor`

By default, DreamStorm send the request to 127.0.0.0:9050 proxy to handle tor connection

## Example

```python
from DreamStorm import DreamStorm

def example_callback(page,headers):
    print "server : " + headers["server"]

C = Connector(5,tor = True) # how many threads to use
C.put(["https://oalieno.github.io","http://www.nctu.edu.tw"])
C.run(example_callback)
```
