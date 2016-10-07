---
type: doc
layout: reference
category: "Syntax"
title: "Returns and Jumps"
---

# 리턴과 점프

코틀린은 3개의 구조적 탈출(Jump) 연산자가 있다. 

* *return*{: .keyword }. 가장 근접하여 감싼 함수(또는 [익명 함수](lambdas.html#anonymous-functions))로부터 빠져나온다.
* *break*{: .keyword }. 가장 근접한 반복문을 빠져나온다.
* *continue*{: .keyword }. 가장 근접한 반복문의 다음 스텝을 수행한다.

## Break and Continue Labels

코틀린의 모든 표현(expression)은 *label*{: .keyword } 을 붙일 수 있다. Label은 `@` 표가 따르는 식별자의 형태를 띈다. 예를 들어, `abc@`, `fooBar@` 는 유효한 Label 이다.([문법](grammar.html#label) 을 참조할 것).
다음과 같이 표현 앞에 label을 위치시키면 표현에 label이 붙는다.

``` kotlin
loop@ for (i in 1..100) {
  // ...
}
```

위와 같이 붙인 label은 *break*{: .keyword } 또는 *continue*{: .keyword } 를 다음과 같이 한정 할 수 있다.

``` kotlin
loop@ for (i in 1..100) {
  for (j in 1..100) {
    if (...)
      break@loop
  }
}
```

A *break*{: .keyword } qualified with a label jumps to the execution point right after the loop marked with that label.
A *continue*{: .keyword } proceeds to the next iteration of that loop.


## Return at Labels

With function literals, local functions and object expression, functions can be nested in Kotlin. 
Qualified *return*{: .keyword }s allow us to return from an outer function. 
The most important use case is returning from a lambda expression. Recall that when we write this:

``` kotlin
fun foo() {
  ints.forEach {
    if (it == 0) return
    print(it)
  }
}
```

The *return*{: .keyword }-expression returns from the nearest enclosing function, i.e. `foo`.
(Note that such non-local returns are supported only for lambda expressions passed to [inline functions](inline-functions.html).)
If we need to return from a lambda expression, we have to label it and qualify the *return*{: .keyword }:

``` kotlin
fun foo() {
  ints.forEach lit@ {
    if (it == 0) return@lit
    print(it)
  }
}
```

Now, it returns only from the lambda expression. Oftentimes it is more convenient to use implicits labels:
such a label has the same name as the function to which the lambda is passed.

``` kotlin
fun foo() {
  ints.forEach {
    if (it == 0) return@forEach
    print(it)
  }
}
```

Alternatively, we can replace the lambda expression with an [anonymous function](lambdas.html#anonymous-functions).
A *return*{: .keyword } statement in an anomymous function will return from the anonymous function itself.

``` kotlin
fun foo() {
  ints.forEach(fun(value: Int) {
    if (value == 0) return
    print(value)
  })
}
```

When returning a value, the parser gives preference to the qualified return, i.e.

``` kotlin
return@a 1
```

means "return `1` at label `@a`" and not "return a labeled expression `(@a 1)`".
