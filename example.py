from DreamStorm import DreamStorm


def example_callback(page, headers):
    print "server : " + headers["server"]


dream = DreamStorm(5, tor=True)
dream.put(["https://oalieno.github.io", "http://www.nctu.edu.tw"])
dream.run(example_callback)
