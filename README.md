# pfactory 0.1.1
## A crappy, incomplete implementation of [factor](http://factorcode.org) as a Python DSL

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