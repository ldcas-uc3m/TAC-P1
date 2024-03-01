# Práctica 1: Máquinas de Turing
By Ignacio Arnaiz Tierraseca & Luis Daniel Casais Mezquida  
Teoría Avanzada de la Computación 23/24  
Bachelor's Degree in Computer Science and Engineering  
Universidad Carlos III de Madrid


## Project statement

La práctica propone el uso de la herramienta JFLAP para diseñar y evaluar diversas Máquinas de Turing. El objetivo es que asimiléis los conceptos impartidos en Magistral para tener un conocimiento claro sobre qué son y para qué sirven Máquinas de Turing Multicinta y No Deterministas, cómo se pueden aplicar al Análisis de Coste Computacional de Algoritmos, las implicaciones que tiene usar una u otra variante, o el uso de una base u otra relacionado con el tamaño de las instancias y la complejidad que se deriva de ellas, etc.  

Las máquinas de Turing deben ser diseñadas y validadas con JFLAP. Para ello usaremos el modo de Input  Multiple Run (Trasducer). Damos por supuesto que todas las máquinas empiezan y terminan con el cabezal situado sobre el símbolo significativo más a la izquierda. De otra forma, la transducción no funcionará correctamente.  
En las versiones multicinta consideraremos que la primera es la que debe contener tanto la palabra inicial como los posibles resultados. Utilizaremos JFLAP 7.1 para el trabajo (JFLAP 7.0 tiene algún problema con las MTND).  

Para facilitar el proceso de contar los pasos de la Máquina de Turing podéis usar
el simulador https://turingmachinesimulator.com/. Podéis usar el script [`jf2txt.py`](src/jf2txt.py) para convertir los diseños de jflap. El simulador sólo sirve para máquinas deterministas, y sólo funciona con JFLAP 7.1.  
Alternativamente se puede usar algún programa para contar clicks de teclado (autoclickers), o para programar series de clicks.  

No se recomienda el uso de Building Block por los problemas que puede causar. Y además dificulta obtener el coste total necesarios para el Análisis de Coste Computacional. 


### 0. Palíndromos
Se plantea uno de los ejemplos vistos en clase magistral:  

Dado el lenguaje $\Sigma = \{a, b\}$, definimos el palíndromo $x$ tal que $x \in \Sigma*$, $|x| = 2k$, $k \in 	\mathbb{Z}^+$, $\exists w \in \Sigma*$, $|w| = k\ |\ x = w \cdot w^{-1}$

Ejemplos de palabras:
- Válidas: λ, aa, bb, aaaa, bbbb, abba, baab, aaaaaa, aabbaa
- Inválidas: ab, ba, aaa, aba, bbb, abb, aabb, abab, baba

Realizar las siguientes tareas para una MT determinista de 1 cinta, de 2 cintas, y para una no determinista de 2 cintas:
1. Implementar el diseño propuesto
2. Determinar cuál es el peor caso en cuanto a coste computacional para un tamaño _n_ dado.
3. Realizar las simulaciones para palabras de diferente tamaño (usando _step_). Preparad la tabla de tamaños de problema y con los pasos obtenidos.
4. Calcular las diferencias finitas.
5. Calcular $T(n)$.
6. Determinar una cota superior asintótica, para $n_0 = 10$.


### 1. Suma de enteros en base uno
La suma dos números enteros $x$ e $y$ representados en base UNO. La cinta inicial contendrá `#x$y#`. Al final sólo debe quedar el valor de $x$ en la cinta (`#x#`). Es obligatorio usar aritmética de Peano (_pred_, _succ_) en todos los apartados. Tened en cuenta que si aplicáis alguna “optimización en el algoritmo de suma, ya no será posible comparar los algoritmos entre sí.  

Estudiad las mejoras obtenidas con las siguientes opciones (realizando las mismas tareas que en el ejercicio anterior):
1. MT Determinista con una cinta
La Máquina de Turing indicada a continuación es un sumador de dos números en base uno. Los dos números están separados por el símbolo `$`. La suma se realiza en base a las operaciones succ y pred de la aritmética de Peano. La primera opera por la derecha de $y$, la segunda por la izquierda de $x$, sobreescribiendo éste valor.

<!-- TODO: image -->
2. MT con dos cintas.

Finalmente evaluar la mejora obtenida con la MT de dos cintas.


### 2. Suma de enteros en base DOS
La suma dos números enteros $x$ e $y$ representados en base DOS. La cinta inicial contendrá `#x$y#`. Al final sólo debe quedar el valor de x en la cinta (`#x#`). Es obligatorio usar aritmética de Peano (_pred_, _succ_) en todos los apartados. Estudiad las mejoras obtenidas con las siguientes opciones (realizando las mismas tareas que en el ejercicio anterior): 
1. MT Determinista con una cinta
La Máquina de Turing indicada a continuación es un sumador de dos números en base dos. Los dos números están separados por el símbolo `$`. La suma se realiza en base a las operaciones _succ_ y _pred_ de la aritmética de Peano. La primera opera sobre $y$, la segunda sobre $x$, dejando en él el resultado. 
<!-- TODO: image -->
2. MT con dos cintas.

Finalmente evaluar la mejora obtenida con la MT de dos cintas.


### 3. Comparativa de los Ejercicios 1 y 2
1. Determinar la eficiencia de cada algoritmo:
Mediante una tabla para comparar los pasos realizados para las sumas con los mismos valores. Es decir, para comparar resultados hay que evaluar en ambas máquinas la misma suma, por ejemplo $3+5$, traducida a la base correspondiente.  
Incluid gráficas superpuestas de los costes para facilitar la comparativa.

La comparativa debe realizarse para máquinas de 1 cinta por un lado, y para las de dos cintas por otro lado.rs
2. ¿Por qué la diferencia de complejidades?
3. ¿Cómo se interpretan las diferencias en complejidad y en eficiencia?


## Installation and execution

1. Check you have Java 8 or higher installed, with `java --version`.  
If you don't, download and install Java Runtime Enviroment with JDK 8+, either the official one or [OpenJDK](https://openjdk.org/).
2. Download [JFLAP](https://www.jflap.org/) 7.1:
   ```bash
   wget https://www.jflap.org/jflaptmp/july27-18/JFLAP7.1.jar
   ```

You can run JFLAP with:
```bash
java -jar JFLAP7.1.jar
```
You can fix scaling errors with the `-Dsun.java2d.uiScale` parameter, e.g.: `java -Dsun.java2d.uiScale=2.0 -jar JFLAP7.1.jar`.


