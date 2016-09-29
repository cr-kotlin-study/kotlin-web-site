---
type: doc
layout: reference
category: "Basics"
title: "Basic Syntax"
---

# Basic Syntax

## Package 선언

Package 선언은 소스파일 최상단에 위치하여야 한다.

``` kotlin
package my.demo

import java.util.*

// ...
```

자바 처럼 패키지 구조와 디렉토리 구조는 일치 할 필요는 없다.

See [Packages](packages.html).

## 함수 선언

2개의 `Int` 인자와 `Int` 리턴 타입을 갖는 함수는 다음과 같다.

``` kotlin
fun sum(a: Int, b: Int): Int {
  return a + b
}
```

함수 표현식과 추론 가능한 리턴 타입을 갖는 함수는 다음과 같이 선언한다.

``` kotlin
fun sum(a: Int, b: Int) = a + b
```
 
함수의 Unit 리턴 타입은 의미 없는 타입을 의미한다.

``` kotlin
fun printSum(a: Int, b: Int): Unit {
  print(a + b)
}
```

`Unit` 타입은 생략 가능하다.

``` kotlin
fun printSum(a: Int, b: Int) {
  print(a + b)
}
```

See [Functions](functions.html).

## 지역 변수 선언

`val` : 한번만 선언하는 지역 변수 (읽기 전용)

``` kotlin
val a: Int = 1
val b = 1   // `Int` type is inferred
val c: Int  // Type required when no initializer is provided
c = 1       // definite assignment
```

`var` : 변경 가능한 지역 변수

``` kotlin
var x = 5 // `Int` type is inferred
x += 1
```

See also [Properties And Fields](properties.html).


## Comments

Java나 Javascript처럼 줄 마지막에 오는 1줄 comment나 block comment를 지원한다.

``` kotlin
// This is an end-of-line comment

/* This is a block comment
   on multiple lines. */
```

Java와는 달리 Kotlin의 block comments 는 can be nested.

See [Documenting Kotlin Code](kotlin-doc.html) for information on the documentation comment syntax.

## String 탬플릿 사용하기

``` kotlin
fun main(args: Array<String>) {
  if (args.size == 0) return

  print("First argument: ${args[0]}")
}
```

See [String templates](basic-types.html#string-templates).

## 조건문 사용하기

``` kotlin
fun max(a: Int, b: Int): Int {
  if (a > b)
    return a
  else
    return b
}
```

Using *if* as an expression:

``` kotlin
fun max(a: Int, b: Int) = if (a > b) a else b
```

See [*if*{: .keyword }-expressions](control-flow.html#if-expression).

## Nullable 값과 Null 체크하기

변수에 Null값이 힐당 가능하려면 타입 뒤에 명시적으로 Null 값이 가능한 변수라고 선언되어 있어야 한다.(type + ?) 

다음 함수는 `str`이 Integer로 변환 불가능 할 경우 Null을 리턴한다.

``` kotlin
fun parseInt(str: String): Int? {
  // ...
}
```

위 함수는 아래와 같이 사용해야 한다.

``` kotlin
fun main(args: Array<String>) {
  if (args.size < 2) {
    print("Two integers expected")
    return
  }

  val x = parseInt(args[0])
  val y = parseInt(args[1])

  // 이곳에서 바로 `x * y`를 수행할 경우 null일 수 있으므로 error가 발생한다.
  if (x != null && y != null) {
    // null check 를 했으므로 여기서 x와 y는 non-nullable값으로 자동 캐스팅 된다.
    print(x * y)
  }
}
```

또는 아래와 같이 사용할 수 있다.

``` kotlin
  // ...
  if (x == null) {
    print("Wrong number format in '${args[0]}'")
    return
  }
  if (y == null) {
    print("Wrong number format in '${args[1]}'")
    return
  }

  // x and y are automatically cast to non-nullable after null check
  print(x * y)
```

See [Null-safety](null-safety.html).

## Using type checks and automatic casts

*is* 연산자는 해당 표현식이 주어진 타입의 instance인지 체크한다. 만약 immutable 지역 변수나 property의 타입이 체크 된 경우, 명시적으로 타입 casting이 필요하진 않다.

``` kotlin
fun getStringLength(obj: Any): Int? {
  if (obj is String) {
    // `obj` 는 이 블록 내에서 `String`으로 자동적으로 캐스팅 된다.
    return obj.length
  }

  // 블록 밖에선 `obj`는 여전히 `Any` type 이다.
  return null
}
```

``` kotlin
fun getStringLength(obj: Any): Int? {
  if (obj !is String)
    return null

  // 이 블록에서는 `obj`는 String이다.
  return obj.length
}
```

또는 아래와 같이 사용할 수 있다.

``` kotlin
fun getStringLength(obj: Any): Int? {
  // && 오른쪽에서는 (이미 왼쪽에서 타입 체크를 했으므로) `obj`는 String이다.
  if (obj is String && obj.length > 0)
    return obj.length

  return null
}
```

See [Classes](classes.html) and [Type casts](typecasts.html).

## Using a `for` loop

``` kotlin
fun main(args: Array<String>) {
  for (arg in args)
    print(arg)
}
```

or

``` kotlin
for (i in args.indices)
  print(args[i])
```

See [for loop](control-flow.html#for-loops).

## Using a `while` loop

``` kotlin
fun main(args: Array<String>) {
  var i = 0
  while (i < args.size)
    print(args[i++])
}
```

See [while loop](control-flow.html#while-loops).

## Using `when` expression

``` kotlin
fun cases(obj: Any) {
  when (obj) {
    1          -> print("One")
    "Hello"    -> print("Greeting")
    is Long    -> print("Long")
    !is String -> print("Not a string")
    else       -> print("Unknown")
  }
}
```

See [when expression](control-flow.html#when-expression).

## Using ranges

Check if a number is within a range using *in*{: .keyword } operator:

``` kotlin
if (x in 1..y-1)
  print("OK")
```

Check if a number is out of range:

``` kotlin
if (x !in 0..array.lastIndex)
  print("Out")
```

Iterating over a range:

``` kotlin
for (x in 1..5)
  print(x)
```

See [Ranges](ranges.html).

## collection 사용하기

Iterating over a collection:

``` kotlin
for (name in names)
  println(name)
```

Checking if a collection contains an object using *in*{: .keyword } operator:

``` kotlin
if (text in names) // names.contains(text) is called
  print("Yes")
```

Using lambda expressions to filter and map collections:

``` kotlin
names
    .filter { it.startsWith("A") }
    .sortedBy { it }
    .map { it.toUpperCase() }
    .forEach { print(it) }
```

See [Higher-order functions and Lambdas](lambdas.html).

