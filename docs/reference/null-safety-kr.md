---
type: doc
layout: reference
category: "Syntax"
title: "Null Safety"
---

# Null Safety

## Nullable 타입과 and Non-Null 타입

코틀린의 타입 시스템은 코드에서 null 참조로 인한 위험성을 제거하는 목표를 갖고 설계되었다.(also known as the [The Billion Dollar Mistake](http://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions) )

자바를 포함한 많은 프로그래밍 언어가 흔히 갖는 함정(pitfalls)은 null을 참조하고 있는 member에 접근하게 하여 결과적으로 null 참조 예외를 발생하는 것이다. (자바에서는 `NullPointerException` 또는 줄여서 NPE로 부르는 것)

코틀린의 타입 시스템은 코드에서 `NullPointerException` 을 제거하기 위해 설계되었다. 코틀린에서의 NPE는 아래의 경우에서만 발생할 수 있다.
* 명시적으로 `throw NullPointerException()` 을 호출했을 때
* `!!`연산자를 아래에서 설명한 방법으로 호출될 떄
* 참조한 자바 코드가 발생시킬 때
* There's some data inconsistency with regard to initialization (an uninitialized *this* available in a constructor is used somewhere)

코틀린에서는, 타입 시스템이 null을 참조 할 수 있는 타입(nullable references)과 null을 참조 할 수 없는 타입(non-null references)을 구분한다. 예를 들어, `String` 타입을 갖는 변수는 null 을 참조할 수 없다.

``` kotlin
var a: String = "abc"
a = null // compilation error
```

Null을 허용하기 위해서는 변수를 nullable string 타입으로 선언해야 한다. 표기는 `String?`와 같이 한다.

``` kotlin
var b: String? = "abc"
b = null // ok
```

위에서 선언된 `a`의 property에 접근할 때에는 NPE를 발생시키지 않을 것이 보장되므로 아래와 같이 안전하게 호출할 수 있다.

``` kotlin
val l = a.length
```
하지만 `b`의 property에 접근할 때는 안전하지 않다고 판단되므로 컴파일 에러를 발생시킨다.

``` kotlin
val l = b.length // error: variable 'b' can be null
```

물론 nullable 타입으로 선언된 변수의 property에 접근하는 것이 당연히 필요할 것이다. 이를 위해서는 다음의 방법들을 이용할 수 있다.

## 조건문을 통한 null 체크
명시적으로 null을 체크한 뒤 null인 경우와 그렇지 않은 경우를 나누어 로직을 수행 할 수 있다.

``` kotlin
val l = if (b != null) b.length else -1
```
위의 경우, 컴파일러는 `b`의 null 여부를 체크한 정보를 이용하여 if문 안에서 `length` 호출을 허용한다. 
다음과 같이 좀 더 복잡한 조건문을 사용할 수 도 있다.

``` kotlin
if (b != null && b.length > 0)
  print("String of length ${b.length}")
else
  print("Empty string")
```

Note that this only works where `b` is immutable (i.e. a local variable which is not modified between the check and the
usage or a member *val*{: .keyword } which has a backing field and is not overridable), because otherwise it might
happen that `b` changes to *null*{: .keyword } after the check.

## Safe Calls

Your second option is the safe call operator, written `?.`:

``` kotlin
b?.length
```
This returns `b.length` if `b` is not null, and *null*{: .keyword } otherwise. The type of this expression is `Int?`.

Safe calls are useful in chains. For example, if Bob, an Employee, may be assigned to a Department (or not),
that in turn may have another Employee as a department head, then to obtain the name of Bob's department head, if any), we write the following:

``` kotlin
bob?.department?.head?.name
```

Such a chain returns *null*{: .keyword } if any of the properties in it is null.

To perform a certain operation only for non-null values, you can use the safe call operator together with [`let`](/api/latest/jvm/stdlib/kotlin/let.html):

``` kotlin
val listWithNulls: List<String?> = listOf("A", null)
for (item in listWithNulls) {
     item?.let { println(it) } // prints A and ignores null
}
```

## Elvis Operator

When we have a nullable reference `r`, we can say "if `r` is not null, use it, otherwise use some non-null value `x`":

``` kotlin
val l: Int = if (b != null) b.length else -1
```

Along with the complete *if*{: .keyword }-expression, this can be expressed with the Elvis operator, written `?:`:

``` kotlin
val l = b?.length ?: -1
```

If the expression to the left of `?:` is not null, the elvis operator returns it, otherwise it returns the expression to the right.
Note that the right-hand side expression is evaluated only if the left-hand side is null.

Note that, since *throw*{: .keyword } and *return*{: .keyword } are expressions in Kotlin, they can also be used on
the right hand side of the elvis operator. This can be very handy, for example, for checking function arguments:

``` kotlin
fun foo(node: Node): String? {
  val parent = node.getParent() ?: return null
  val name = node.getName() ?: throw IllegalArgumentException("name expected")
  // ...
}
```

## The `!!` Operator

The third option is for NPE-lovers. We can write `b!!`, and this will return a non-null value of `b`
(e.g., a `String` in our example) or throw an NPE if `b` is null:

``` kotlin
val l = b!!.length
```

Thus, if you want an NPE, you can have it, but you have to ask for it explicitly, and it does not appear out of the blue.

## Safe Casts

Regular casts may result into a `ClassCastException` if the object is not of the target type.
Another option is to use safe casts that return *null*{: .keyword } if the attempt was not successful:

``` kotlin
val aInt: Int? = a as? Int
```

## Collections of Nullable Type

If you have a collection of elements of a nullable type and want to filter non-null elements, you can do so by using `filterNotNull`.

``` kotlin
val nullableList: List<Int?> = listOf(1, 2, null, 4)
val intList: List<Int> = nullableList.filterNotNull()
```
