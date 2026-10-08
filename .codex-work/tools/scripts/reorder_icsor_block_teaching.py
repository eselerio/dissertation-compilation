from pathlib import Path

p = Path('article/chapters/05_interpretable_surrogate.tex')
t = p.read_text(encoding='utf-8')
a = t.index('For fixed \\(B\\) and \\(\\widehat C\\), define \\(E=\\widehat C-\\Phi B^\\top\\). The coupling proposal solves')
b = t.index('The coupling calculation can be read one output row at a time.', a)
c = t.index('For fixed \\(B\\) and \\(\\Gamma\\), the fitted-state update separates over the training rows.', b)
compact = t[a:b]
definition = 'For fixed \\(B\\) and \\(\\widehat C\\), define \\(E=\\widehat C-\\Phi B^\\top\\).'
compact = compact.replace(definition+' The coupling proposal solves', 'Collecting these scalar residuals across all output rows gives the coupling proposal', 1)
t = t[:a] + definition + '\n\n' + t[b:c] + compact + t[c:]

a = t.index('For fixed \\(B\\) and \\(\\Gamma\\), the fitted-state update separates over the training rows.')
b = t.index('The quadratic-program method of \\citet{Stellato2018}', a)
block = t[a:b]
eq_start = block.index('\\begin{equation}')
eq_end = block.index('\\end{equation}', eq_start) + len('\\end{equation}')
formula = block[eq_start:eq_end]
row_start = block.index('Each row minimizes', eq_end)
exp_start = block.index('The matrix and vector in Equation~\\eqref{eq:icsor_state_update}', row_start)
square_start = block.index('Completing the square explains', exp_start)
row = block[row_start:exp_start]
expansion = block[exp_start:square_start]
expansion = expansion.replace('The matrix and vector in Equation~\\eqref{eq:icsor_state_update} follow by expanding the three residual sums for one observation.', 'Expand the three residual sums for one observation before collecting their coefficients.',1)
intro = 'For fixed \\(B\\) and \\(\\Gamma\\), the fitted-state update separates over the training rows. For sample \\(i\\), write \\(\\widehat c_i\\) as a column vector.\n\n'
scalar = r'''Write the expanded quadratic as \(\widehat c_i^\top H_C\widehat c_i-2h_i^\top\widehat c_i\). The entry \((H_C)_{fg}\) is the coefficient of a product of component coordinates in that quadratic, and \((h_i)_f\) supplies its linear term. Let \(\delta_{fg}\) equal one when \(f=g\) and zero otherwise. Reading the coefficients entry by entry gives
\begin{equation}
\label{eq:icsor_state_scalar_coefficients}
\begin{aligned}
(H_C)_{fg}&=\delta_{fg}+\lambda_{inv}\sum_{k=1}^{K}A_{kf}A_{kg}
+\lambda_{sys}\sum_{j=1}^{F}R_{jf}R_{jg},\\
(h_i)_f&=c_{out,if}
+\lambda_{inv}\sum_{k=1}^{K}A_{kf}\sum_{g=1}^{F}A_{kg}c_{in,ig}\\
&\quad+\lambda_{sys}\sum_{j=1}^{F}R_{jf}\sum_{\ell=1}^{D}B_{j\ell}\phi_{i\ell}.
\end{aligned}
\end{equation}
For example, the invariant contribution to \((H_C)_{12}\) adds the product of the first and second component weights over the invariant rows. The system contribution adds the product of columns 1 and 2 of \(R\). These products explain why correcting one fitted component can change the preferred value of another.

'''
example = block[square_start:]
tail = 'The general coefficient arrays derived above are assembled in the compact form\n' + formula + '\n' + row
t = t[:a] + intro + expansion + scalar + example + tail + t[b:]
p.write_text(t,encoding='utf-8')
print('Moved scalar coupling and fitted-state teaching before compact updates.')
