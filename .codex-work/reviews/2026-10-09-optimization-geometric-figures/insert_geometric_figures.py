"""Integrate mathematical figures without changing empirical result content.

Run from dissertation-compilation. This one-time editing record requires the
pre-figure source and refuses to write if Results and discussion changes.
"""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "article/compile/optimization/manuscript.tex"
before = path.read_bytes()
text = before.decode("utf-8")
if r"\label{fig:concept-balances}" in text:
    raise RuntimeError("figures already integrated; preserve the current source")


def append_to_paragraph(prefix, addition):
    global text
    pattern = "^" + re.escape(prefix) + r"[^\r\n]*"
    text, count = re.subn(pattern, lambda match: match.group() + addition,
                         text, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"expected one paragraph starting {prefix!r}, got {count}")


append_to_paragraph(
    r"When $\xi_i=0$,",
    r"""

Figure~\ref{fig:concept-balances} distinguishes the geometric roles of the mixer and reactor balances. The mixer concentration is a convex combination of its incoming compositions. In a reactor without external additions, conversion preserves the affine set defined by $Ac_i=Ac_{i-1}$. Reaction directions are tangent to this set, while the invariant rows are normal to it. The kinetic equations determine which points on the set represent steady operation.

\begin{figure}[pos=htbp]
\centering
\includegraphics[width=\linewidth]{concept_balance_geometry.pdf}
\caption{Dimensionless two-component illustration of network balances. (a) For $r_I=2$ and $r_R=1$, Equation~\eqref{eq:mixer} gives $m=0.25x+0.50c_N+0.25c_U$, inside the convex hull of the incoming compositions. (b) With no external addition and invariant normal $a=(1,1)^\top/\sqrt{2}$, the illustrated reactor responses remain on $\zeta_1+\zeta_2=1.2$. The reaction direction is orthogonal to $a$. The points illustrate conservation geometry rather than solutions of the reaction-rate equations.}
\label{fig:concept-balances}
\end{figure}
""",
)

append_to_paragraph(
    r"For the ordered endpoints $X_E\le X_U$,",
    r"""

The geometric reduction in Figure~\ref{fig:concept-inventory} maps many admissible layer profiles to one inventory interval. The extremal profiles attain its endpoints, and profiles inside the envelope can have nonmonotone layer concentrations. The width of the interval decreases to zero as the two outlet concentrations approach one another.

\begin{figure}[pos=htbp]
\centering
\includegraphics[width=\linewidth]{concept_clarifier_inventory.pdf}
\caption{Clarifier inventory geometry for ten equal-volume layers and an arbitrary positive concentration scale $X_{\rm ref}$. (a) At $X_E/X_{\rm ref}=0.2$ and $X_U/X_{\rm ref}=2$, a nonmonotone example satisfies the endpoint envelope. Assigning every internal layer to either endpoint gives the lower and upper inventory extremizers; connecting segments only guide the eye between discrete layers. (b) At fixed $X_E/X_{\rm ref}=0.2$, the shaded band contains exactly the normalized mean inventories allowed by Equation~\eqref{eq:inventoryenvelope}. The two bounds coincide when $X_U=X_E$. Envelope-admissible profiles need not satisfy the nonlinear settling-flux equations.}
\label{fig:concept-inventory}
\end{figure}
""",
)

append_to_paragraph(
    "Enforcing constraints does not by itself establish greater prediction accuracy",
    r"""

In coordinates $\zeta=D_\chi^{-1}\chi$, Equation~\eqref{eq:projection} minimizes the Euclidean distance from the standardized raw response to the feasible set. Figure~\ref{fig:concept-projection} shows this nearest-point geometry and the effect of an additional closure equality. Positivity of a closure target alone does not ensure that its equality intersects the remaining constraints.

\begin{figure}[pos=htbp]
\centering
\includegraphics[width=\linewidth]{concept_joint_projection.pdf}
\caption{Projection and closure compatibility in an illustrative standardized response space. The constraint set is $\mathcal C_0=\{\zeta\in\mathbb R_+^2:\zeta_1+\zeta_2=1\}$. (a) The raw response $\zeta_{\rm raw}=(1.20,0.55)$ projects to $\zeta^\star=(0.825,0.175)$; circles denote equal distance from $\zeta_{\rm raw}$. The dashed line extends the affine balance beyond its nonnegative segment. (b) Adding $\zeta_1=0.35$ gives the feasible point $(0.35,0.65)$. Adding $\zeta_1=1.20$ instead requires $\zeta_2=-0.20$, so the intersection is empty despite a positive closure target.}
\label{fig:concept-projection}
\end{figure}
""",
)

append_to_paragraph(
    r"Here $\mathcal V$ contains",
    r"""

Figure~\ref{fig:concept-active-set} illustrates how a projected response can remain continuous while its derivative changes at an active-set transition. For a fixed polyhedron and an affine raw-response path, the projection is piecewise affine. In the plant model, the constraint operators and right-hand side also depend on the controls; local differentiability therefore requires regularity of the active constraints and verification of the derivative calculation.

\begin{figure}[pos=htbp]
\centering
\includegraphics[width=\linewidth]{concept_active_set.pdf}
\caption{Active-set geometry of an analytical parametric projection. The response minimizes $\tfrac12\|\zeta-\zeta_{\rm raw}(t)\|_2^2$ over $\{\zeta\in\mathbb R_+^2:\zeta_1+\zeta_2=1\}$, with $\zeta_{\rm raw}(t)=(t,1-t)$. (a) The solution is $\zeta_1^\star(t)=\min\{1,\max\{0,t\}\}$ and $\zeta_2^\star=1-\zeta_1^\star$. (b) Its derivative is zero, one, and zero on the three open active-set intervals. At $t=0$ and $t=1$, the active bound has zero multiplier and unequal one-sided derivatives; open markers denote the undefined derivative.}
\label{fig:concept-active-set}
\end{figure}
""",
)

text = text.replace(r"\section{Methodology}",
                    "\\FloatBarrier\n\n" + r"\section{Methodology}", 1)
text = text.replace(
    r"\subsection{Raw plant-response regression and overflow solids model}",
    "\\FloatBarrier\n\n" + r"\subsection{Raw plant-response regression and overflow solids model}",
    1,
)

after = text.encode("utf-8")
start, end = br"\section{Results and discussion}", br"\section{Conclusions}"
protected_before = before[before.index(start):before.index(end)]
protected_after = after[after.index(start):after.index(end)]
if protected_before != protected_after:
    raise RuntimeError("empirical Results and discussion changed; refusing to write")
for filename in (
    "concept_balance_geometry.pdf", "concept_clarifier_inventory.pdf",
    "concept_joint_projection.pdf", "concept_active_set.pdf",
):
    if not (path.parent / filename).is_file():
        raise FileNotFoundError(filename)
path.write_bytes(after)
print("Integrated four figures beside manuscript.tex; protected result hash:",
      hashlib.sha256(protected_after).hexdigest())
