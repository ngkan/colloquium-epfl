---
title: The PCP theorem
author: ''
aspect_ratio: '16:9'
footer:
  left: ''
  center: ''
  right: auto
---

<!-- layout: title-left -->

# The PCP theorem

Local verification and hardness of approximation

<!-- notes: The talk explains how local proof checks lead to approximation gaps. The Set Cover argument assumes a regular form of Label Cover and a deterministic construction of a covering gadget. -->

---

## 3-SAT asks whether one assignment satisfies every clause

A Boolean variable has value $0$ or $1$. A literal is a variable $x$ or its negation $\neg x$.

A 3-SAT formula is an AND of clauses. Each clause is an OR of three literals, on three distinct variables.

$$ \phi=(x_1\lor\neg x_2\lor x_3)\land(\neg x_1\lor x_2\lor x_4). $$

| Term | Meaning |
| --- | --- |
| Assignment | One Boolean value for each variable |
| Satisfied clause | At least one literal has value $1$ |
| Yes-instance | Some assignment satisfies every clause |
| No-instance | Every assignment violates at least one clause |

We use basic probability, sets, graphs, and asymptotic notation. Let $n$ denote input length. Let $m$ denote the number of clauses.

<!-- notes: The displayed formula is satisfiable. For example, assigning 1 to all four variables satisfies both clauses. Input length includes the encoding of variable indices, signs, and clauses. The restriction to three distinct variables per clause still gives an NP-complete problem. -->

---

## Checking a solution differs from finding a solution

For 3-SAT, a proposed assignment is a certificate for a yes-answer. The verifier evaluates every clause to check the certificate.

| Complexity class | Definition for decision problems |
| --- | --- |
| $\mathrm{P}$ | An algorithm decides yes or no in polynomial time |
| $\mathrm{NP}$ | A verifier checks a certificate of polynomial length in polynomial time |

For a problem in $\mathrm{NP}$, a yes-instance has an accepted certificate. A no-instance has no accepted certificate.

```box
title: Definition
tone: blue
content: |
  A reduction transforms one problem into another while preserving the answer. A polynomial-time reduction takes polynomial time.
```

Every problem in $\mathrm{NP}$ reduces to 3-SAT in polynomial time.

A polynomial-time 3-SAT algorithm would therefore imply $\mathrm{P}=\mathrm{NP}$.

<!-- notes: A problem is NP-hard if every problem in NP reduces to it in polynomial time. The reductions in the first part of this talk preserve a yes/no promise. The final Set Cover reduction has a larger running time, which we state explicitly. -->

---

## A constant gap separates two promised cases

Define $\operatorname{val}(\phi)$ as the largest fraction of clauses that one assignment satisfies.

| Problem | Yes-case | No-case |
| --- | --- | --- |
| Ordinary 3-SAT | $\operatorname{val}(\phi)=1$ | $\operatorname{val}(\phi)\le 1-1/m$ |
| Gap 3-SAT | $\operatorname{val}(\phi)=1$ | $\operatorname{val}(\phi)\le 1-\varepsilon$ |

Here $\varepsilon>0$ is a fixed constant. A promise means that the input belongs to one of the two stated cases.

```box
title: Remark
tone: green
content: |
  Suppose an algorithm satisfies more than a $1-\varepsilon$ fraction of clauses on every satisfiable input. Its output would distinguish the two Gap 3-SAT cases.
```

Our first goal is a polynomial-time reduction from ordinary 3-SAT to Gap 3-SAT.

<!-- notes: An unsatisfiable formula with m clauses can have value as high as 1-1/m. The constant gap applies to the output of the reduction. It need not hold for arbitrary unsatisfiable formulas. The algorithm in the remark must return an actual assignment. On a promised no-instance, no assignment can exceed the threshold. -->

---

<!-- layout: section-break -->

## Local verification

How can a few proof queries detect a false claim?

---

## A PCP verifier reads a few bits of an encoded proof

PCP means **probabilistically checkable proof**. The proof is a bit string of polynomial length that supports random checks of a yes-claim.

| Ordinary certificate check | PCP check |
| --- | --- |
| Read the proposed assignment | Access an encoded proof by position |
| Check all clauses | Choose a test at random |
| Accept if every clause holds | Read a constant number of proof bits. Test those bits. |

The prover fixes the proof before the verifier chooses its random bits. The verifier can also read the full input formula.

```box
title: Remark
tone: green
content: |
  Sampling a few clauses of an ordinary formula can miss its only violated clause. The PCP theorem uses a different proof format.
```

<!-- notes: The proof has polynomial length. Random access means that the verifier can request a bit at a specified position without reading the preceding bits. The verifier takes polynomial time in the input length. A constant query bound limits proof access, not access to the input. The prover cannot change the proof after the verifier chooses the random test. -->

---

## The PCP theorem guarantees detection with constant probability

Let $n$ be the input length. The verifier uses $O(\log n)$ random bits and reads at most $q$ proof bits, for a constant $q$.

```box
title: Theorem
tone: blue
content: |
  Every problem in $\mathrm{NP}$ has such a polynomial-time verifier, with the following guarantees.\*
```

| Input | Guarantee over the verifier's random choices | Name |
| --- | --- | --- |
| Yes-instance | Some proof always passes | Perfect completeness |
| No-instance | Every proof passes with probability at most $s<1$ | Soundness bound $s$ |

The constants $q$ and $s$ do not depend on $n$. For a no-instance, the verifier therefore rejects every proof with probability at least $1-s$.

The verifier checks a supplied proof. It does not find that proof or decide the problem without one.

<!-- footnote: \* Arora–Safra and Arora–Lund–Motwani–Sudan–Szegedy (1998). -->
<!-- notes: References: https://doi.org/10.1145/273865.273901 and https://doi.org/10.1145/278298.278306 . The probability concerns only the verifier's randomness, for each fixed input and proof. The soundness guarantee applies to every proof of a no-instance. It does not require rejection of every badly formed proof of a yes-instance. The usual notation for this result is NP=PCP(O(log n),O(1)). -->

---

## Random proof checks give a formula with a constant gap

Start with a 3-SAT input $\phi$. The PCP verifier supplies tests of a proposed proof for $\phi$.

1. Use each proof bit as a Boolean variable.
2. Make one constraint for each possible random choice of the verifier. The constraint requires that test to accept.
3. Convert each constraint into a constant number of 3-SAT clauses, with additional variables.

There are only $2^{O(\log n)}=n^{O(1)}$ tests. Each test depends on a constant number of proof bits.

If a proof passes a test, additional variable values can satisfy all clauses for that test. Otherwise, every choice violates at least one clause.

| Input $\phi$ | Output formula $\psi$ |
| --- | --- |
| Satisfiable | Some proof passes every test, and some assignment satisfies all output clauses |
| Unsatisfiable | Every proof fails a constant fraction of tests, so every assignment violates at least an $\varepsilon$ fraction of clauses |

We use the standard clause conversion without proving it. From now on, the clause–variable game uses $\psi$, the Gap 3-SAT output.

<!-- notes: A constraint is a condition on a small group of variables. For each fixed random string, the verifier defines a Boolean condition on a constant number of proof positions. A constant-size decision tree represents all possible answers to adaptive queries, and a constant-size 3-CNF encoding uses new auxiliary variables for each test. Passing tests permit an extension satisfying all clauses, while failed tests force a violated clause under every extension. Thus a constant fraction of failed tests gives a constant fraction of violated clauses. See Arora and Barak, Computational Complexity: A Modern Approach, section 11.3.1. -->

---

## Two provers must agree about the same variable

For the gap formula $\psi$, the verifier selects a clause $C_i$ uniformly. It then selects one of that clause's variables $x_j$ uniformly.

| | Prover 1 | Prover 2 |
| --- | --- | --- |
| Question | The clause $C_i$ | The variable $x_j$ |
| Answer | Values for its three variables | One Boolean value $b$ |

The provers agree on a strategy before the test. They cannot communicate after they receive their questions.

```box
title: Definition
tone: blue
content: |
  The verifier accepts exactly when both conditions hold:

  - Prover 1's answer satisfies $C_i$.
  - Prover 1's value for $x_j$ equals prover 2's answer $b$.
```

If $\psi$ is satisfiable, both provers can answer from the same satisfying assignment. The verifier then always accepts.

<!-- notes: Prover 1 does not learn which variable the verifier selected. Prover 2 does not learn the clause. A deterministic strategy specifies one answer for each possible question. Literal signs determine whether the returned variable values satisfy the clause. -->

---

## A no-instance causes rejection with probability at least ε/3

```box
title: Proof
tone: purple
content: |
  Fix deterministic strategies. Prover 2 gives one fixed answer for each variable. These answers define a global assignment $z$.

  In a no-instance, $z$ violates at least an $\varepsilon$ fraction of clauses. Consider one such clause.

  If prover 1's answer does not satisfy the clause, the verifier rejects. Otherwise, that answer differs from $z$ on at least one variable.

  The verifier selects that variable with probability at least $1/3$. Thus

  $$ \Pr[\text{reject}]\ge\varepsilon\cdot\frac13,\qquad
  \Pr[\text{accept}]\le 1-\frac{\varepsilon}{3}.\quad\square $$
```

Randomized strategies are mixtures of deterministic strategies. The same bound therefore applies to them.

<!-- notes: Prover 1 must choose its answer without knowing which of the three variables the verifier will select. This restriction gives the factor 1/3. The probability of selecting a clause false under z is at least epsilon. Randomness shared before the game cannot improve on the best deterministic strategy. -->

---

## The clause–variable game becomes a graph problem

1. Create one left vertex for each clause.
2. Create one right vertex for each variable.
3. Connect each clause vertex to its variable vertices.

| Game | Graph representation |
| --- | --- |
| Prover 1's answer to a clause | A label at the clause vertex |
| Prover 2's answer to a variable | A label at the variable vertex |
| One verifier test | An edge between that clause and variable |

A left label is an assignment that satisfies its clause. A right label is one Boolean value.

```box
title: Definition
tone: blue
content: |
  For an edge $e=(u,v)$, the map $\pi_e$ extracts the value for variable $v$ from the clause label at $u$.
```

The labels satisfy an edge exactly when the label at $v$ equals $\pi_e$ applied to the label at $u$.

The verifier selects every edge with equal probability. Thus the fraction of satisfied edges equals the game's acceptance probability.

<!-- notes: For each clause on three distinct variables, exactly seven local assignments satisfy it. A common alphabet of size seven can encode these assignments. Each clause vertex has three edges. Uniformly selecting a clause and then a variable selects an edge uniformly. Thus the fraction of satisfied edges equals the game's acceptance probability. -->

---

## Label Cover asks for labels that satisfy many edges

```box
title: Definition
tone: blue
content: |
  Let $G=(L\cup R,E)$ be a bipartite graph. Write $V=L\cup R$ for all vertices.

  The alphabets $A$ and $B$ are the finite sets of allowed left and right labels. Each edge has a map $\pi_e:A\to B$.
```

A labeling assigns $\sigma_L(u)\in A$ to each $u\in L$ and $\sigma_R(v)\in B$ to each $v\in R$.

$$ \text{The labeling satisfies }e=(u,v)\text{ exactly when }\pi_e\bigl(\sigma_L(u)\bigr)=\sigma_R(v). $$

The value $\operatorname{val}(G)$ is the largest fraction of edges that one labeling satisfies.

For the clause–variable game, the yes-case has value $1$. The no-case has value at most $1-\varepsilon/3$.

<!-- notes: The objective is to maximize the number of satisfied edges. Dividing by the fixed number of edges gives the same approximation ratio. The general definition permits larger alphabets than the original clause–variable game. The map pi_e specifies the unique right label consistent with each left label. -->

---

## Parallel repetition makes the no-case value smaller

Repeat the game on independent questions. Each prover answers all its questions at once. The verifier accepts only if all repeated tests accept.

Provers can correlate their answers across repetitions. The next theorem bounds their success despite these correlations.

```box
title: Theorem
tone: blue
content: |
  For an integer parameter $\ell\ge1$, a constant multiple of $\ell$ repetitions gives the following SAT-to-Label-Cover reduction.\*
```

| Property | Bound, for original SAT input length $n$ |
| --- | --- |
| Yes-case | $\operatorname{val}(G)=1$ |
| No-case | $\operatorname{val}(G)\le 2^{-\ell}$ |
| Alphabet sizes | $\lvert A\rvert,\lvert B\rvert=2^{O(\ell)}$ |
| Construction time and instance size | $n^{O(\ell)}$ |

<!-- footnote: \* Raz (1998), A Parallel Repetition Theorem. -->
<!-- notes: https://doi.org/10.1137/S0097539795280895 . After repetition, vertices represent tuples of questions and labels represent tuples of answers. Coordinatewise projections preserve the Label Cover form. The base game has a constant gap and constant alphabets. Its repeated value decreases as exp(-Omega(t)), so a suitable constant multiple of ell repetitions gives the displayed bound. The size of the gap formula is polynomial in the original input length n. -->

---

## An approximation within a fixed factor would decide SAT

For this maximization problem, a $c$-approximation returns a labeling with value at least $\operatorname{val}(G)/c$, where $c>1$.

```box
title: Proof
tone: purple
content: |
  Fix $c$. Choose a constant $\ell$ with $2^{-\ell}<1/c$.

  In the yes-case, the algorithm must return value at least $1/c$. In the no-case, no labeling has value above $2^{-\ell}$.

  We can therefore decide the original SAT input by comparing the returned value with $1/c$. The reduction takes polynomial time because $\ell$ is constant. $\square$
```

```box
title: Proposition
tone: blue
content: |
  For every fixed $c>1$, a polynomial-time $c$-approximation for Label Cover would imply $\mathrm{P}=\mathrm{NP}$.
```

<!-- notes: The algorithm must return a feasible labeling, whose value we can compute. The strict separation 2^(-ell)<1/c leaves no ambiguity at the threshold. The statement concerns each fixed factor c. -->

---

<!-- layout: section-break -->

## The Set Cover reduction

How can inconsistent labels make a cover large?

---

## Set Cover minimizes the number of selected sets

```box
title: Definition
tone: blue
content: |
  The input contains a universe $\mathcal U$ and a family of its subsets. A cover is a subfamily whose union equals $\mathcal U$.

  The objective is to select as few sets as possible. Write $\operatorname{OPT}_{\mathrm{SC}}$ for this minimum.
```

For example, $\{1,2\}$ and $\{2,3\}$ cover the universe $\{1,2,3\}$.

A factor-$\rho$ approximation returns a cover with at most $\rho\operatorname{OPT}_{\mathrm{SC}}$ sets. This is a minimization guarantee.

| Our reduction should achieve | Required cover size |
| --- | --- |
| Label Cover value $1$ | At most one set per vertex |
| Label Cover value very small | Many more sets per vertex on average |

We will build a small set system, called a gadget, that turns agreement between labels into a small cover.

<!-- notes: The input lists the available subsets. Algorithms can select only those subsets. A maximization guarantee divides the optimum by the approximation factor. A minimization guarantee multiplies the optimum by that factor. We will create a separate copy of the gadget for each graph edge. -->

---

## A gadget forces small covers to use a complementary pair

A pair $C_i,\overline{C_i}$ is complementary when $\overline{C_i}=U\setminus C_i$. The pair always covers $U$.

```box
title: Lemma
tone: blue
content: |
  For positive integers $r,k$, there is a universe $U$ with $r$ complementary pairs

  $$ C_1,\overline{C_1},\ldots,C_r,\overline{C_r}. $$

  Every cover with at most $k$ sets contains a complementary pair.
```

Thus a cover without a complementary pair needs more than $k$ sets. The parameter $k$ sets this lower bound on the cover size.

The next two slides prove that such a gadget exists. A later step separately assumes an efficient deterministic construction.

<!-- notes: We use r for the number of pairs to distinguish it from the clause count m. A complementary pair means both indexed sets C_i and its complement for the same i. The lemma concerns subfamilies of the displayed indexed set family. -->

---

## A fixed family is unlikely to cover a random gadget

Let $M=|U|$. For every element and index $i$, independently include the element in $C_i$ with probability $1/2$.

```box
title: Proof
tone: purple
content: |
  Fix $t\le k$ sets with no complementary pair. They use $t$ distinct indices.

  For one element, each selected set misses it with probability $1/2$. The $t$ membership choices are independent.

  $$ \Pr[\text{all selected sets miss this element}]=2^{-t}\ge2^{-k}. $$

  The family covers $U$ only if it misses no element. Independence across the $M$ elements gives

  $$ \Pr[\text{family covers }U]\le(1-2^{-k})^M\le e^{-M/2^k}.\quad\square $$
```

<!-- notes: Selecting a complement reverses one membership bit but preserves its probability 1/2. The absence of a complementary pair ensures distinct indices and therefore independence for one element. The final inequality uses 1-x<=exp(-x). -->

---

## A union bound gives one gadget that works for all families

We must exclude every cover of size at most $k$ that contains no complementary pair.

There are at most $(2r+1)^k$ candidate families. Encode a family by at most $k$ set indices. Fill unused positions with an empty symbol.

```box
title: Proof
tone: purple
content: |
  The union bound says that the probability of any failure is at most the sum of the individual failure probabilities.

  $$ \Pr[\text{some forbidden family covers }U]\le(2r+1)^k e^{-M/2^k}. $$

  Choose $M\ge2^k\bigl(k\ln(2r+1)+\ln2\bigr)$. The failure probability is at most $1/2$, so some gadget has the required property. $\square$
```

This proves existence. It does not supply the deterministic construction used in the reduction.

<!-- notes: Sort the indices in each family. Then add empty symbols. This gives an injection into strings of length k over 2r+1 symbols. Counting all such strings overestimates the number of families, which is sufficient. Use the smallest integer that is at least M. -->

---

## The remaining reduction needs two construction assumptions

Choose an integer $k\ge2$. We need a no-case Label Cover value $\delta\le2/k^2$.

```box
title: Assumption
tone: red
content: |
  Assume that the SAT-to-Label-Cover reduction produces a $D$-regular graph, with $D>0$. Every vertex then has exactly $D$ incident edges.

  Assume the same completeness, soundness, size, and running-time bounds as before.
```

```box
title: Assumption
tone: red
content: |
  Assume a deterministic construction of the gadget with $r$ pairs, size $\operatorname{poly}(r,2^k)$, and running time $\operatorname{poly}(r,2^k)$.
```

Here $\operatorname{poly}$ means a fixed polynomial. The proof assumes both constructions. We do not prove these construction assumptions here.

<!-- notes: The earlier game analysis alone does not establish the regular form. This slide makes that additional input explicit before the counting argument uses it. The final hardness consequence is conditional on these stated constructions. We will choose ell so that the no-case bound 2^(-ell) is at most 2/k^2. -->

---

## Each vertex and label define one available set

For each edge $e=(u,v)$, create a separate gadget $U^e$. Use $r=|B|$ pairs, one for each right label $b\in B$.

The full universe is the union of these disjoint copies: $\mathcal U=\bigsqcup_{e\in E}U^e$.

| Vertex and label | Available set |
| --- | --- |
| Left: $u\in L$, $a\in A$ | $S_{u,a}=\displaystyle\bigcup_{e\ni u}C^e_{\pi_e(a)}$ |
| Right: $v\in R$, $b\in B$ | $S_{v,b}=\displaystyle\bigcup_{e\ni v}\overline{C^e_b}$ |

The notation $e\ni u$ means that edge $e$ touches vertex $u$. Each available set combines one part from every incident edge gadget.

```box
title: Remark
tone: green
content: |
  Inside $U^e$, left sets contain parts $C^e_{\pi_e(a)}$ and right sets contain complements $\overline{C^e_b}$. No other vertex has sets that intersect $U^e$.
```

<!-- notes: Keep each available set indexed by its vertex and label, even if two indices define equal subsets. A cover can choose one index for each selected subset without increasing its size. This convention makes the later count of labels equal to the number of selected sets. -->

---

## A satisfying labeling needs at most one set per vertex

Suppose $\operatorname{val}(G)=1$. Fix a labeling that satisfies every edge.

For $e=(u,v)$, write $a=\sigma_L(u)$ and $b=\sigma_R(v)$. The edge condition gives $\pi_e(a)=b$.

| Selected set | Its part inside $U^e$ |
| --- | --- |
| $S_{u,a}$ | $C^e_b$ |
| $S_{v,b}$ | $\overline{C^e_b}$ |
| Their union | $U^e$ |

```box
title: Proof
tone: purple
content: |
  Select the set for each vertex's label. Every edge receives a complementary pair, so these sets cover every gadget.

  There is at most one selected set per vertex. Thus $\operatorname{OPT}_{\mathrm{SC}}\le |V|$. $\square$
```

<!-- notes: The cover is complete because the edge gadgets form the full universe. The inequality is an upper bound, not an assertion that the optimum equals |V|. This is the completeness direction of the reduction. -->

---

## An arbitrary cover gives each vertex a list of labels

Now suppose $\operatorname{val}(G)\le\delta\le2/k^2$. Let $\mathcal C$ be any cover of the constructed universe.

For each vertex $w$, record the labels of its selected sets:

$$ \Lambda_w=\{a:S_{w,a}\in\mathcal C\}. $$

| Object | Good | Bad |
| --- | --- | --- |
| Vertex $w$ | $\lvert\Lambda_w\rvert\le k/2$ | $\lvert\Lambda_w\rvert>k/2$ |
| Edge $(u,v)$ | Both endpoints are good | At least one endpoint is bad |

Each selected set has one vertex index. Hence $|\mathcal C|=\sum_{w\in V}|\Lambda_w|$.

We will prove that many vertices are bad. Each bad vertex forces the cover to contain more than $k/2$ sets.

<!-- notes: Lambda_w is a set of labels, which we call a list. The label alphabet depends on the side containing w. A list can be empty. The terms good and bad describe list length, not whether a labeling satisfies a particular edge. -->

---

## A good edge has a consistent pair in its endpoint lists

```box
title: Proof
tone: purple
content: |
  Let $e=(u,v)$ be good. Only sets indexed by $u$ or $v$ can intersect $U^e$.

  The two lists have at most $k/2$ labels each. Thus at most $k$ selected sets cover $U^e$.

  The gadget property forces a complementary pair $C^e_b,\overline{C^e_b}$. A left label $a$ with $\pi_e(a)=b$ supplies $C^e_b$.

  The right label $b$ supplies the complement. Therefore

  $$ \text{some }a\in\Lambda_u\text{ and }b\in\Lambda_v\text{ satisfy }\pi_e(a)=b.\quad\square $$
```

Both endpoint lists are nonempty. The next step converts these local pairs into one labeling of the whole graph.

<!-- notes: Multiple left labels can project to the same right label. This only reduces the number of distinct gadget parts in a cover. The gadget property still applies. The existence of a complementary indexed pair ensures a label on each side. -->

---

## Random labels limit the number of good edges

Choose one label independently and uniformly from each nonempty list. Assign any label to a vertex with an empty list.

```box
title: Proof
tone: purple
content: |
  Each good edge has at least one consistent pair in its lists. The probability of choosing that pair is

  $$ \frac{1}{|\Lambda_u|\,|\Lambda_v|}\ge\frac{1}{(k/2)^2}=\frac{4}{k^2}. $$

  Let $g$ be the number of good edges. Add their success probabilities to bound the expected number of satisfied edges:

  $$ \mathbb E[\text{number of satisfied edges}]\ge\frac{4g}{k^2}. $$

  Every labeling satisfies at most $\delta|E|$ edges. The expected number satisfies the same upper bound:

  $$ \frac{4g}{k^2}\le\delta|E|\le\frac{2|E|}{k^2},\qquad g\le\frac{|E|}{2}.\quad\square $$
```

<!-- notes: The expectation symbol E denotes the average over the random label choices. Linearity of expectation does not require independent edge events. The choices at different vertices are independent, which gives the probability for a fixed consistent pair. Empty lists do not occur at endpoints of good edges. -->

---

## Many bad edges require many bad vertices

At least $|E|/2$ edges are bad. Let $V_{\mathrm{bad}}$ be the set of bad vertices.

```box
title: Proof
tone: purple
content: |
  Each bad edge touches a bad vertex. Each bad vertex touches exactly $D$ edges. Thus

  $$ \frac{|E|}{2}\le D|V_{\mathrm{bad}}|. $$

  Counting both endpoints of every edge gives $2|E|=D|V|$. Substitute this identity into the inequality to obtain $|V_{\mathrm{bad}}|\ge|V|/4$.

  Each bad vertex contributes more than $k/2$ selected sets. Therefore

  $$ |\mathcal C|>\frac{k}{2}|V_{\mathrm{bad}}|\ge\frac{k|V|}{8}.\quad\square $$
```

<!-- step -->

The Set Cover gap is now explicit: the yes-case has optimum at most $|V|$, and the no-case has optimum greater than $k|V|/8$.

<!-- notes: The inequality can count an edge twice when both endpoints are bad. Double counting is valid because we need an upper bound on the number of bad edges incident to bad vertices. Regularity converts the edge count into a vertex count. -->

---

## More repetitions support a larger covering gap

The gap factor is $k/8$. Increasing $k$ also requires a smaller no-case value, because we need $2^{-\ell}\le2/k^2$.

For sufficiently large original input length $n$, choose

$$ k=\left\lceil\log_2 n\,\log_2\log_2 n\right\rceil,
\qquad \ell=\left\lceil4\log_2\log_2 n\right\rceil. $$

| Quantity | Size |
| --- | --- |
| $2^{-\ell}$ | At most $(\log_2 n)^{-4}$ |
| $k^2$ | $\Theta((\log n)^2(\log\log n)^2)$ |

The factor $(\log n)^2$ eventually exceeds $(\log\log n)^2$. Hence the soundness requirement holds for all sufficiently large $n$.

We can handle small input sizes separately. The reduction has gap $k/8=\Theta(\log n\,\log\log n)$.

<!-- notes: With these choices, 2^ell is at least (log_2 n)^4. The ratio 2^ell/k^2 tends to infinity. Thus 2^(-ell)<=2/k^2 for all sufficiently large n. Round both parameters to integers. A finite number of smaller input sizes does not affect the asymptotic complexity statement. -->

---

## The covering gap is logarithmic in the output universe

Let $N=|\mathcal U|$ be the number of elements in the Set Cover universe. The approximation ratio depends on $N$, the output size, rather than $n$, the input size.

| Construction step | Size and time bound |
| --- | --- |
| Label Cover instance | $n^{O(\ell)}$ |
| One edge gadget, with $r=\lvert B\rvert$ | $\operatorname{poly}(r,2^k)$ |
| All edge gadgets and vertex sets | $n^{O(\ell)}\operatorname{poly}(r,2^k)$ |

Since $\ell=\Theta(\log\log n)$ and $k=\Theta(\log n\,\log\log n)$, the total bound is

$$ n^{O(\log\log n)}=2^{O(k)}. $$

In particular, $N\le2^{O(k)}$, so $\log N=O(k)$. Therefore the gap satisfies $k/8=\Omega(\log N)$.

<!-- notes: The alphabet size r is 2^{O(ell)}. The bound n^{O(ell)} includes polynomial factors in the Label Cover instance size. It includes the time to list the elements of every available set. The bound n^{O(log log n)} is quasipolynomial. It is larger than the polynomial-time bound needed for a usual NP-hardness reduction. -->

---

## A better approximation would decide SAT

Assume the two constructions stated earlier. Suppose a deterministic polynomial-time algorithm returns covers of size at most $\rho(N)\operatorname{OPT}_{\mathrm{SC}}$, where $\rho(N)=o(\log N)$.

The notation $o(\log N)$ means that $\rho(N)/\log N$ tends to zero as $N$ increases. Since $k/8=\Omega(\log N)$, eventually $\rho(N)\lt k/8$.

| Original SAT input | Cover returned by the algorithm |
| --- | --- |
| Yes-instance | Fewer than $(k/8)\lvert V\rvert$ sets |
| No-instance | More than $(k/8)\lvert V\rvert$ sets, because every cover is this large |

The cover size therefore decides SAT. Both the reduction and the approximation algorithm take $n^{O(\log\log n)}$ time on this constructed input.

```box
title: Proposition
tone: blue
content: |
  Under the stated construction assumptions, a deterministic polynomial-time $o(\log N)$-approximation for Set Cover would give a deterministic $n^{O(\log\log n)}$-time SAT algorithm.
```

<!-- notes: Assume a deterministic approximation algorithm. Its polynomial running time in the constructed input size remains n^{O(log log n)}. For bounded N, solve Set Cover exactly by enumerating all subfamilies of distinct available subsets. There are at most 2^N distinct subsets, so bounded N requires only a constant number of subfamilies. The conclusion becomes an inapproximability statement if we assume SAT has no such deterministic algorithm. This argument does not establish the sharp modern Set Cover threshold. -->

---

## The reduction uses local consistency at every step

| Step | What the proof establishes |
| --- | --- |
| PCP verifier | In a no-instance, every proof fails a constant fraction of tests |
| Gap 3-SAT game | In a no-instance, every prover strategy fails a constant fraction of consistency tests |
| Parallel repetition | Every labeling satisfies at most a small fraction of edges in a no-instance |
| Covering gadget | A small cover of an edge gadget forces a consistent pair of labels |
| Random labels and regularity | Low Label Cover value forces a large Set Cover solution |

The central link is the complementary pair: consistent labels cover an edge gadget with two sets.

A no-instance forces at least one quarter of the vertices to use long lists. Those lists make every cover large.

<!-- notes: The construction assumptions remain essential to the final complexity consequence. -->

---

## Further reading

<!-- size: small -->

- S. Arora and S. Safra (1998). [Probabilistic checking of proofs: A new characterization of NP](https://doi.org/10.1145/273865.273901).
- S. Arora, C. Lund, R. Motwani, M. Sudan, and M. Szegedy (1998). [Proof verification and the hardness of approximation problems](https://doi.org/10.1145/278298.278306).
- R. Raz (1998). [A Parallel Repetition Theorem](https://doi.org/10.1137/S0097539795280895).
- C. Lund and M. Yannakakis (1994). [On the hardness of approximating minimization problems](https://doi.org/10.1145/185675.306789).
- S. Arora and B. Barak (2009). *Computational Complexity: A Modern Approach*, Chapter 11.

<!-- notes: These references cover the PCP theorem, its gap formulation, parallel repetition, and hardness of approximation. The presentation uses the regular Label Cover reduction and deterministic gadget construction as explicit assumptions. -->
