---
title: Convexity and concentration
author: ''
aspect_ratio: '16:9'
figure_captions: true
footer:
  left: ''
  center: ''
  right: auto
---

<!-- layout: title-left -->

# Convexity and concentration

Geometry, descent, and finite-sample guarantees

EPFL · Mathematics seminar

<!-- notes: A short mathematical talk that demonstrates the EPFL theme. The examples connect convex geometry, a gradient step, and a finite-sample probability bound. -->

---

<!-- layout: section-break -->

## Geometry of convex functions

A first-order inequality gives a bound on the objective decrease.

<!-- notes: Introduce the two conditions. Convexity describes the geometry. Smoothness controls the change along a step. -->

---

## Two inequalities describe the geometry

```box
title: Definition
tone: blue
content: |
  A differentiable function $f:\mathbb{R}^d\to\mathbb{R}$ is convex if, for all $x,y\in\mathbb{R}^d$,

  $$ f(y) \ge f(x)+\langle\nabla f(x),y-x\rangle. $$
```

```box
title: Assumption
tone: red
content: |
  The gradient is $L$-Lipschitz, with $L>0$. Consequently,

  $$ f(y) \le f(x)+\langle\nabla f(x),y-x\rangle+\frac L2\|y-x\|_2^2. $$
```

<!-- notes: Convexity gives the lower bound. Smoothness gives the upper bound. The next descent result needs smoothness alone. -->

---

## A gradient step decreases the objective

Consider $x^+=x-\eta\nabla f(x)$, where $0<\eta\le 1/L$.

```box
title: Theorem
tone: blue
content: |
  If $f$ has an $L$-Lipschitz gradient, then\*

  $$ f(x^+) \le f(x)-\frac{\eta}{2}\|\nabla f(x)\|_2^2. $$
```

A small enough step decreases the objective whenever the gradient is nonzero.

<!-- footnote: \* Background: Nesterov, Introductory Lectures on Convex Optimization (2004), Chapter 2. -->

<!-- notes: This one-step result does not require convexity. Convexity helps us obtain global convergence guarantees from bounds on the objective decrease. -->

---

## The proof is one substitution

```box
title: Proof
tone: purple
content: |
  Let $g=\nabla f(x)$. Apply the smoothness inequality with $y=x-\eta g$:

  $$
  \begin{aligned}
  f(x-\eta g)
  &\le f(x)-\eta\|g\|_2^2+\frac{L\eta^2}{2}\|g\|_2^2 \\
  &= f(x)-\eta\left(1-\frac{L\eta}{2}\right)\|g\|_2^2 \\
  &\le f(x)-\frac{\eta}{2}\|g\|_2^2 \\
  &\le f(x).
  \end{aligned}\qquad\square
  $$
```

<!-- step -->

The key condition is $L\eta\le 1$.

<!-- notes: This slide demonstrates an optional reveal. The slide shows the derivation immediately. The next advance shows the takeaway. PDF export includes both. -->

---

<!-- columns: 45/55 -->

## Read the inequalities geometrically

### Convexity bounds both sides

The graph lies **above a tangent** and **below a chord**.

$$
f((1-t)x+ty)\le (1-t)f(x)+tf(y)
$$

For $0\le t\le1$, interpolation gives an upper bound on the function value.

|||

![For f(z) = z²/4, the tangent at 1 lies below the graph. The chord from −2 to 3 lies above the graph between those endpoints.](assets/convexity.svg)

<!-- notes: The tangent is a lower bound on the entire graph. The chord is an upper bound only on the interval between its endpoints. -->

---

## Finite-sample guarantees for empirical averages

Let $X_1,\ldots,X_n$ be independent, with $X_i\in[0,1]$ almost surely.

$$ \bar X_n=\frac1n\sum_{i=1}^nX_i,\qquad \mu=\frac1n\sum_{i=1}^n\mathbb E[X_i]. $$

```box
title: Proposition
tone: blue
content: |
  Hoeffding's inequality gives, for every $\varepsilon>0$,\*

  $$ \mathbb P\!\left(\left|\bar X_n-\mu\right|\ge\varepsilon\right)\le 2\exp(-2n\varepsilon^2). $$
```

For failure probability at most $\delta\in(0,1)$, it suffices to take $n\ge\log(2/\delta)/(2\varepsilon^2)$.

<!-- footnote: \* Hoeffding (1963), Probability inequalities for sums of bounded random variables, Theorem 2. -->

<!-- notes: This is the layout stress test: a long heading, sums with subscripts, expectation, tall delimiters, and a probability bound. The variables need not have identical distributions. The sufficient sample size makes the failure probability at most delta. -->

---

## References and further reading

<!-- size: small -->

1. Yurii Nesterov (2004). *Introductory Lectures on Convex Optimization: A Basic Course.* Springer.\
   [doi:10.1007/978-1-4419-8853-9](https://doi.org/10.1007/978-1-4419-8853-9)
2. Wassily Hoeffding (1963). *Probability inequalities for sums of bounded random variables.* Journal of the American Statistical Association, 58(301), 13–30.\
   [doi:10.1080/01621459.1963.10500830](https://doi.org/10.1080/01621459.1963.10500830)


<!-- notes: References use normal hyperlinks. The slides and equations themselves remain available offline. -->
