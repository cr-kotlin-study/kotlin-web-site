---
type: doc
layout: reference
category: "Classes and Objects"
title: "Data Classes"
---

# Data Classes

우리는 종종 데이터의 값을 갖는 것 이외의 다른 일을 하지 않는 클래스를 생성한다. 그러한 클래스의 경우 몇몇의 표준화된 functionality가 기계적으로(mechanically) 따라온다. Kotlin에서는 이러한 클래스를 _data class_ 라고 부르며 다음과 같이 클래스에 `data` 를 표기하여 구분한다.:
 
``` kotlin
data class User(val name: String, val age: Int)
```

Data Classes에 대해 컴파일러는 primary constructor에 선언된 모든 properties로 부터 다음의 member들을 생성한다. 
  
  * `equals()`와 `hashCode()`, 
  * `"User(name=John, age=42)"`과 같은 형태의 `toString()`,
  * [`componentN()` functions](multi-declarations.html) corresponding to the properties in their order of declaration,
  * `copy()` function (see below).
  
위의 항목들이 클래스 내부나 상속된 base class에 명시적으로 정의되어 있다면 자동으로 생성하지 않는다.

생성된 코드의 To ensure consistency and meaningful behavior를 위하여 data classes는 다음 조건을 만족해야 한다.

  * Primary constructor는 적어도 하나의 파라미터를 갖아야 한다.
  * 모든 primary constructor의 파라미터는 `val` 또는 `var` 로 표기되어야 한다.
  * Data classes는 abstract, open, sealed 또는 inner 일 수 없다.
  * Data classes는 다른 클래스를 상속받지 않는다. ( 단, 인터페이스를 구현하기는 한다.)
  
> 만약 JVM에서 생성된 클래스가 파라미터 없는 빈 생성자를 가져야 한다면, 모든 properties에 대해 기본값을 명시해 주면 된다.
> (see [Constructors](classes.html#constructors)).
>
> ``` kotlin
> data class User(val name: String = "", val age: Int = 0)
> ```

## Copying
  
It's often the case that we need to copy an object altering _some_ of its properties, but keeping the rest unchanged. 
This is what `copy()` function is generated for. For the `User` class above, its implementation would be as follows:
     
``` kotlin
fun copy(name: String = this.name, age: Int = this.age) = User(name, age)     
```     

This allows us to write

``` kotlin
val jack = User(name = "Jack", age = 1)
val olderJack = jack.copy(age = 2)
```

## Data Classes and Destructuring Declarations

_Component functions_ generated for data classes enable their use in [destructuring declarations](multi-declarations.html):

``` kotlin
val jane = User("Jane", 35) 
val (name, age) = jane
println("$name, $age years of age") // prints "Jane, 35 years of age"
```

## Standard Data Classes

The standard library provides `Pair` and `Triple`. In most cases, though, named data classes are a better design choice, 
because they make the code more readable by providing meaningful names for properties.
