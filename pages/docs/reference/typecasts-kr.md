---
type: doc
layout: reference
category: "Syntax"
title: "Type Checks and Casts"
---

# 타입 체크와 타입 변환

## `is` 와 `!is` 연산자

실행 시점(runtime)에 객체가 주어진 타입에 맞는지(conforms) 체크하기 위해서는 `is` 연산자를, 맞지 않는지 체크하기 위해서는 `!is` 연산자를 사용할 수 있다.

``` kotlin
if (obj is String) {
  print(obj.length)
}

if (obj !is String) { // !(obj is String) 과 같다.
  print("Not a String")
}
else {
  print(obj.length)
}
```

## Smart 타입 변환
코틀린에서는 대부분의 경우 명시적 타입 변환을 사용 할 필요가 없다. 왜냐하면 컴파일러가 불변인(immutable) 값에 `is` 연산자를 통해 수행한 타입 체크를 추적하여 필요할 경우 (안전한) 타입 변환을 자동적으로 수행하기 때문이다.

``` kotlin
fun demo(x: Any) {
  if (x is String) {
    print(x.length) // x 는 String 타입으로 변환된다.
  }
}
```

컴파일러는 return 이 수반된 `!is` 연산자의 수행인 경우에도 타입 변환을 수행한다.

``` kotlin
  if (x !is String) return
  print(x.length) // x 는 String 타입으로 변환된다.
```

더 나아가, `is` + `&&` 또는 `!is` + `||` 의 오른쪽 비교 (나중에 수행되는 비교) 구문에서도 타입 변환을 수행한다.

``` kotlin
  // `||` 오른쪽 비교구문에서 x 는 String 타입으로 변환된다. 
  if (x !is String || x.length == 0) return

  // `&&` 오른쪽 비교구문에서 x 는 String 타입으로 변환된다. 
  if (x is String && x.length > 0)
      print(x.length) // x is automatically cast to String
```

컴파일러가 자동적으로 수행하는 타입 변환은 [*when*{: .keyword }-expressions](control-flow.html#when-expressions)
과 [*while*{: .keyword }-loops](control-flow.html#while-loops) 에서도 적용될 수 있다.

``` kotlin
when (x) {
  is Int -> print(x + 1)
  is String -> print(x.length + 1)
  is IntArray -> print(x.sum())
}
```

Smart 타입 변환은 컴파일러가 보기에 변수의 체크 시점과 사용 시점 사이에 변수 값의 변화가 없다고 보장되지 않은 상황에서는 적용되지 않는다. 
좀 더 구체적인 규칙은 다음과 같다.

  * *val*{: .keyword } local variables - always;
  * *val*{: .keyword } properties - if the property is private or internal or the check is performed in the same module where the property is declared. Smart casts aren't applicable to open properties or properties that have custom getters;
  * *var*{: .keyword } local variables - if the variable is not modified between the check and the usage and is not captured in a lambda that modifies it;
  * *var*{: .keyword } properties - never (because the variable can be modified at any time by other code).


## "Unsafe" 타입 변환 연산자
보통, 타입 변환 연산자는 변환이 불가능할 경우 exception을 발생시키기 때문에 *unsafe*한 타입 변환 이라고 부른다.
코틀린에서 Unsafe한 타입 변환은 삽입 연산자(infix operator) `as` 를 이용해 이뤄진다. (see [operator precedence](grammar.html#operator-precedence)):

``` kotlin
val x: String = y as String
```

null은 `String` 타입으로 변환될 수 없다. 왜냐하면 `Stirng` 타입은 not nullable 이기 때문이다. [nullable](null-safety.html)
예를 들어, 만약 `y` 가 null일 경우 exception이 발생한다.
Java의 타입 변환과 같은 의미를 갖으려면 아래와 같이 오른쪽 타입을 null을 허용하는 타입으로 선언해야 한다.

``` kotlin
val x: String? = y as String?
```

## "Safe" (nullable) 타입 변환 연산자
Exception 발생을 피하기 위해서는, *safe* 타입 변환 연산자를 이용할 수 있다. *as?* 는 *safe* 타입 변환 연산자로, 타입 변환에 실패할 경우 null을 반환한다.

``` kotlin
val x: String? = y as? String
```
*as?* 오른쪽 타입이 String이지만 형 변환에 실패할 경우 null을 갖기 때문에 x 의 타입은 String이 아니라 String? 이 된다.