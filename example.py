from DreamStorm import DreamStorm
from DreamStorm.lib.modules.Pager import Pager

def example_callback(package, page, headers):
    print package["url"]

pager = Pager()

dream = DreamStorm(10, tor=False)
dream.put(["http://oalieno.github.io"])
dream.run(example_callback,pager.callback)
