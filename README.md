# pfactory 0.1.1
## A crappy, incomplete implementation of [Factor][0] as a Python DSL

This was inspired by Jon Purdy's, “[Why Concatenative Programming Matters](http://evincarofautumn.blogspot.mx/2012/02/why-concatenative-programming-matters.html)”

Example code:

```python
    assert parse("3 2 -")() == 1
    assert parse("2 -")(3) == 1
    assert parse("3 2 *")() == 6
    assert parse("2 3 * 4 5 * +")() == 26
    
    countWhere = parse("filter len")
    assert countWhere(lambda x: x < 3, range(5)) == 3
    
    # python's filter kind of sucks for use in factor because 
    # the data is not the first argument
    fltr = lambda data, fn: filter(fn, data)
    countWhere = parse("fltr len")
    assert parse("[2 >] countWhere")([1,2,3,4,5,]) == 3
```

### Additional Notes

This is a learning exercise, not a library intended for actual use. 

If someone likes this and wants to work on it - cool! - but just know, you're 
probably better off just using the real [Factor Compiler][0] and calling it
as a subprocess :)


[0]: http://factorcode.org
