# DreamStorm

A Crawler Library

Support : 
- multi-thread
- tor

## Get Started 

`pip install DreamStorm`

## Scripts

[scripts](/scripts) folder is some script I wrote using DreamStorm library

## Dependency

### tor

`apt-get install tor`

By default, DreamStorm send the request to 127.0.0.0:9050 proxy to handle tor connection

### beautifulsoup4

If `pip install DreamStorm` **did not** install beautifulsoup4 as well, use the following command

`pip install beautifulsoup4`

### lxml

you might need to install lxml using following command

`pip install lxml`

## Example

```python
from DreamStorm import DreamStorm
from DreamStorm.lib.modules.Pager import Pager

def example_callback(package, page, headers):
    print package["url"]

pager = Pager()

dream = DreamStorm(10, tor=False) # 10 means 10 threads
dream.put(["https://oalieno.github.io"])
dream.run(example_callback,pager.callback)
```

pager is a built-in module that can automated crawl through all page in the domain

## Document

### callback function

A callback function is call when the response is back and you can start handling the response

It should have three parameter

package -> the original request being sent, it's a dictionary

```
package = {
    "url": "https://oalieno.github.io",
    "headers": {...},
    "postdata": {...}
}
```
page -> the response html page, it's just a string

headers -> the response headers, it's a dictionary

you can return a dictionary in callback function which represent the new package to be requested

### DreamStorm.put

`put(self, url, headers = None, postdata = None)`

first parameter accept `str` or `dict` or `[str,dict,...]`

second parameter accept `dict` ( global headers to all urls in this put action )

third parameter accept `dict` ( global postdata to all urls in this put action )

example : 

`dream.put("https://oalieno.github.io")`

`dream.put({ "url": "https://oalieno.github.io", "headers": {...}, "postdata": {...} })` -> local headers and postdata with certain url

`dream.put(["https://oalieno.github.io",{ "url": "http://www.nctu.edu.tw", "headers": {...} },...])`
