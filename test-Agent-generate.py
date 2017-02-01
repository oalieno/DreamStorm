from lib.core.Agent import Agent

A = Agent({
    "url" : "https://aaa.com",
    "mutations" : 5,
    "mutable-query" : {"a" : 1},
    "stable-query" : {},
    "stable-header" : {},
    "mutable-header" : {},
    "stable-postdata" : {},
    "mutable-postdata" : {"user" : "aaa"}
})

result = A.generate("https://oalieno.github.io")

for i in result:
    print i
