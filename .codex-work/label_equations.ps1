param([switch]$Apply, [string]$WorkspaceRoot, [string[]]$Chapters = @('03', '04', '05', '06'))

$ErrorActionPreference = 'Stop'
$root = if ($WorkspaceRoot) { $WorkspaceRoot } else { Split-Path $PSScriptRoot -Parent }
$expected = @{ '03' = 33; '04' = 27; '05' = 72; '06' = 195 }
$titles = @{}
$titles['03'] = @'
Fixed ordering of the twenty component concentrations
Idealized aerobic oxidation of an organic unit
Idealized oxidation of biomass with ammonium release
Idealized ammonium oxidation to nitrite
Idealized nitrite oxidation to nitrate
Idealized overall nitrification reaction
Idealized nitrate denitrification with an organic donor
Idealized nitrite denitrification with an organic donor
Idealized anaerobic ammonium oxidation reaction
Dimensions and orientation of the stoichiometric matrix
Vector and scalar reaction contributions to component rates
Monod substrate saturation factor
Representative growth rate with substrate and oxygen limitation
Steady-state reactor component equation
Effluent change expressed through reaction and oxygen transfer
Hydraulic dilution rate from retention time
Oxygen-transfer coefficient from the aeration setting
Net oxygen-transfer rate and saturation concentration
Zero reaction contribution to a stoichiometric invariant
Singular-value decomposition of the stoichiometric matrix
Numerical threshold for stoichiometric rank
Orthonormal mass conservation operator from the null space
Null-space and orthonormality identities of the invariant operator
Reactor invariant equation including oxygen transfer
Compatibility of oxygen forcing with mass conservation
Equality of influent and effluent invariant inventories
Invariant inventory change with an external source
Reaction-progress coordinates for the effluent change
Equivalent reaction and invariant-null spaces
Component-state set satisfying mass conservation and non-negativity
Component-to-water-quality reporting map
Control-volume component equation with transport and reaction
One-dimensional advection-diffusion-reaction component equation
'@ -split '\r?\n'
$titles['04'] = @'
Reactor surrogate inputs from operation and influent concentrations
Raw component-state prediction from a fitted surrogate
Row-group penalty for multiresponse regression coefficients
Observation counts for nested reactor assessment
Positive provisional target and relative projection weights
Null-space parameterization of states satisfying mass conservation
Weighted least-squares problem for projection coordinates
Normal equations for weighted projection coordinates
Component candidate satisfying mass conservation
Candidate direction from the feasible influent anchor
Interpolation bound for a decreasing concentration
Interpolation factor and final state satisfying non-negativity
Mass conservation identity for the final projected state
Numerical mass conservation and non-negativity acceptance checks
Raw and projected water-quality composites
Component error standardized by the training response scale
Normalized mean squared component error
Normalized root mean squared component error
Normalized mean absolute component error
Component and macro-average coefficients of determination
Mass conservation residual and standardized negative concentration
Mass conservation and non-negativity violation frequencies
Jointly feasible fraction of assessed component states
Paired difference in projected and raw prediction error
Standardized component displacement caused by projection
Normalized trapezoidal area under a learning curve
Input exceedance beyond an upper training-domain bound
'@ -split '\r?\n'
$titles['05'] = @'
Illustrative component changes for a two-component reaction
Illustrative stoichiometric matrix and mass conservation operator
Structured-regression mass conservation operator from the null space
Effluent change in stoichiometric process coordinates
Mass conservation equality for the structured-regression effluent
Structured-regression feasible set for mass conservation and non-negativity
Illustrative operating, influent, and mixed Kronecker products
Second-order driver feature vector and its dimension
Numerical evaluation of an illustrative regression driver
Scalar polynomial form of the illustrative regression driver
Matrix mapping from second-order features to the regression driver
Driver decomposition into operating, influent, and interaction blocks
Illustrative driver with aeration, nitrogen, and interaction effects
Expansion of a two-variable quadratic form
Numerical example of quadratic-coefficient symmetrization
Symmetric representation of a quadratic form
Frobenius-norm decomposition into symmetric and skew parts
Illustrative coupled equations for two effluent components
Illustrative coupling matrix and coupled-state system
Inverse of the illustrative two-component coupling system
General coupled-state relation and system matrix
Diagonal, magnitude, and conditioning safeguards for component coupling
Squared Frobenius norm as a sum of coefficient squares
Scalar expansion of the structured-regression training objective
Matrix form of the structured-regression training objective
Illustrative numerical contributions to the training penalties
Regularized least-squares objective for one driver coefficient row
Scalar stationarity conditions for a driver coefficient row
Normal equations for the driver coefficient row
Illustrative scalar ridge objective and its polynomial expansion
Closed-form ridge update for the driver coefficient matrix
Illustrative scalar coupling objective and its expansion
Regularized least-squares update for component coupling
Scalar entries of the fitted-state Hessian and forcing vector
Completed-square form of the fitted-state objective
Hessian and forcing vector for the fitted-state update
Raw deployed state from the fitted coupled system
Mass conservation and non-negativity diagnostics of a deployed state
Lagrangian for an illustrative two-component affine projection
Stationarity and equality conditions for the illustrative affine projection
Closed-form solution of the illustrative affine projection
Euclidean affine projection onto the mass conservation equality
Closed-form affine projection of the raw component state
Illustrative matrix of the mass conservation projection
Absolute-adjustment bounds for an illustrative two-component projection
Weighted absolute-distance projection for mass conservation and non-negativity
Water-quality composites of the final checked state
Illustrative driver coefficients and operating-dependent driver
Illustrative transformation of driver coefficients through coupling
Illustrative composite coefficients after coupling
Raw component-response coefficients after coupling
Raw composite-response coefficients after coupling and reporting
Gradients of the illustrative scalar regression driver
Illustrative propagation of an operating derivative through coupling
Illustrative operating Jacobians before and after coupling
Component driver expressed through symmetric quadratic matrices
Operating and influent gradients of a component driver
Raw component and composite Jacobians after coupling
Illustrative operating derivative after affine projection
Complementary mass conservation projection matrices
Operating and influent Jacobians of the affine-projected state
Illustrative affine-projected components as functions of an operating input
Percentage frequency of a physical-constraint violation
Per-composite squared, root, and absolute error measures
Mean relative absolute error of a reported composite
Coefficient of determination for a reported composite
Root mean squared error pooled across four reported composites
Observation counts for structured-regression sample-size assessment
Trapezoidal approximation of normalized learning-curve area
Integral definition of normalized learning-curve area
Mean dense ranks over quantities, measures, and sample sizes
Held-out minus training root-error gap
'@ -split '\r?\n'
$titles['06'] = @'
Reactor-train flow including both recycle streams
Clarifier-feed flow after mixed-liquor recycle withdrawal
Clarifier underflow split into return sludge and waste sludge
Effluent flow after waste withdrawal
Plant flow ratios relative to fresh-influent flow
Scalar mixer equation for one component
Mixer concentration as a flow-weighted component average
Illustrative two-component mixer matrix equation
Vector mixer equation for the complete component state
Illustrative component inventory entering the mixer
Illustrative mixer concentration after flow normalization
Stage retention times and recycle-adjusted dilution rates
Dynamic reactor-stage equation for one component
Steady-state reactor-stage equation for one component
Vector reactor-stage equation with aeration and external additions
Illustrative stoichiometric matrix and normalized invariant row
Illustrative cancellation of the reaction contribution to an invariant
Illustrative steady-state equation for the consumed component
Illustrative steady-state equation for the produced component
Reaction, oxygen-forcing, and rank identities of the plant invariant operator
Scalar cancellation of reaction rates in an invariant equation
Scalar reactor-stage invariant equation with external additions
Invariant inventory change across one reactor stage
Accumulated invariant change across the reactor train
Reactor-train invariant equation and external-addition total
Reactor-train invariant equation after mixer substitution
Invariant equation after cancellation of mixed-liquor recycle
Clarifier-feed invariant flow equals the two outlet invariant flows
External plant mass conservation after internal recycle cancellation
Alkalinity-related invariant combination
Metal-related invariant combination
Illustrative soluble and particulate component selectors
Illustrative coordinate projectors from the component selectors
Completeness and orthogonality identities of the component selectors
Scalar mass conservation across the clarifier
Flow-weighted clarifier outlet component responses
Joint clarifier component and soluble-transport equalities
Flow-weighted soluble component in the overflow
Equality of overflow and feed soluble concentrations
Particulate densification requirement for the underflow
Bounds on the fraction of feed particulate material recovered in underflow
Overflow solids bound implied by particulate densification
Feed, overflow, and underflow suspended-solids concentrations
Bounded double-exponential settling velocity
Illustrative solids equation for the upper clarifier layer
Illustrative solids equation for the clarifier feed layer
Illustrative solids equation for the lower clarifier layer
Particulate outlet reconstruction from endpoint solids concentrations
Illustrative four-layer clarifier solids inventory
General clarifier solids inventory and total volume
Interior-layer solids envelope between the outlet concentrations
Lower inventory bound for two illustrative interior layers
Upper inventory bound for two illustrative interior layers
Lower total-inventory bound for an illustrative four-layer clarifier
Upper total-inventory bound for an illustrative four-layer clarifier
Lower clarifier-inventory bound from endpoint concentrations
Upper clarifier-inventory bound from endpoint concentrations
Admissible interval for the clarifier solids inventory
Inventory represented by a common interior-layer concentration
Solids inventory of the illustrative ten-layer clarifier
Lower inventory bound for the illustrative ten-layer clarifier
Upper inventory bound for the illustrative ten-layer clarifier
Illustrative joint response of a one-stage, two-component plant
Complete joint plant-response vector and its dimension
Mechanistic reactor-and-clarifier state vector and its dimension
Illustrative standardization of a control and an influent concentration
Standardized plant input vector and its dimension
Illustrative quadratic product matrix of two standardized inputs
Illustrative unique-monomial second-order feature vector
Linear and unique-quadratic feature coordinates
Centered and scaled plant regression feature vector
Dimension of the unique-monomial plant feature vector
Scalar expansion of the multiresponse ridge objective
Matrix form of the multiresponse ridge fitting problem
Raw joint plant prediction on the physical response scale
Normal equations for one ridge response coordinate
Dimensionless logarithmic overflow-solids target
Ridge fitting problem for the logarithmic overflow model
Positive overflow-solids prediction from logarithmic back-transformation
Illustrative logarithmic average and geometric concentration mean
Illustrative mixer equality for the soluble component
Illustrative mixer equality for the particulate component
Illustrative reactor mass conservation equality
Illustrative clarifier equality for the soluble component
Illustrative clarifier equality for the particulate component
Illustrative soluble underflow transport equality
Illustrative empirical overflow-solids equality
Matrix form of the illustrative plant projection equalities
Illustrative joint response satisfying the plant projection equalities
Joint mixer, reactor-invariant, and clarifier projection equalities
Empirical overflow-solids closure equality
Illustrative lower inventory bound in outlet-flow coordinates
Illustrative upper inventory bound in outlet-flow coordinates
Matrix form of illustrative densification and inventory inequalities
General densification and clarifier-inventory projection inequalities
Standardized projection displacement of one response coordinate
Scaled mixer equation before the return-sludge term
Return-sludge term and target of the scaled mixer equation
Minimum-distance objective for joint plant projection
Reconstruction of the projected physical plant response
Illustrative weighted projection with mass conservation and non-negativity
Illustrative projection stationarity for the first component
Illustrative projection stationarity for the second component
Illustrative projection equality for the component total
Standardized matrices of the illustrative two-component projection
Standardized quadratic projection with equalities and inequalities
Stationarity condition for the plant quadratic projection
Complementarity condition for the projection inequality multipliers
Completed-square expansion of the projection Lagrangian
Target terms in the completed-square projection Lagrangian
Dual objective of the standardized quadratic projection
Primal-dual gap and its non-negative decomposition
Illustrative cancellation of the stationarity residual
Illustrative inequality slack vector
Illustrative value of the primal projection objective
Illustrative value of the dual projection objective
Weighted response norm from coordinate scales
Variational inequality characterizing a Euclidean projection
Coordinatewise squared-error decomposition
Cross term in the coordinatewise squared-error decomposition
Squared-error bound for a feasible reference
Weighted error reduction bound when the reference is projection-feasible
Distance from the reference state to the projection set
Cross-term decomposition using a projected reference
Reference-infeasibility term in the cross-term decomposition
Product of projection displacement and reference infeasibility
Squared-error bound including reference infeasibility
Upper error bound using squared reference infeasibility
Distance bound when the reference is not projection-feasible
Scalar equality-constrained projection with a varying parameter
Optimality system for the scalar parametric projection
Derivative system for the scalar parametric projection
Numerical example of the parametric projection derivative
Linear system for a fixed active set of projection constraints
Differentiated stationarity for a control-dependent active set
Differentiated feasibility for a control-dependent active set
Joint sensitivity system for a control-dependent active set
Derivative of the control-dependent overflow-solids target
Effluent component-to-water-quality map
Scalar expansion of the weighted effluent-quality objective
Vector form of the weighted effluent-quality objective
Normalized retention-time and aeration objective terms
Normalized mixed-liquor and return-sludge recycle objective terms
Normalized waste-solids objective term
Scalar expansion of the six-term engineering objective
Vector engineering objective and normalized priority weights
Aeration objective for the illustrative equal-volume reactor train
Declared engineering and effluent-quality priority vectors
External solids loss through effluent and waste sludge
Plant solids retention time from inventory and external loss
Illustrative effluent solids-loss calculation
Illustrative waste-sludge solids-loss calculation
Clarifier surface and solids loading measures
Underflow, feed-solids, and external-loss safeguards
Illustrative regularized feature Gram matrix
Root-mean-square standardized projection displacement diagnostic
Ridge feature-leverage diagnostic
Particulate split-consistency diagnostic
Scaled reactor-equation residual diagnostic
Term-based scale for an independently checked residual
Surrogate-assisted plant operating optimization problem
McCormick inequalities for a bounded bilinear product
Illustrative direct reactor equation for the consumed component
Illustrative direct reactor equation for the produced component
Interior-layer envelope residuals for direct optimization
Direct mechanistic plant operating optimization problem
Exact maximum and minimum expressed through absolute values
Smooth approximation of a maximum
Smooth approximation of a minimum
Smooth approximation of the positive-part function
Regularized smooth approximation of a quotient
Rationalization of the smoothed positive-part expression
Cancellation-resistant form of the smoothed positive part
Quintic receiver switch and its transition coordinate
Smoothing and receiver-width continuation sequence
Illustrative recycle-dependent soluble mixer concentration
Illustrative two-stage reactor Jacobian with recycle coupling
Central finite-difference approximation of a Jacobian entry
Second-order forward finite-difference approximation of a Jacobian entry
Tridiagonal sparsity pattern of the clarifier-layer Jacobian
Seven freely varied controls of the connected-plant case
Conversion of a uniform integer to open-unit jitter
Ten-layer initial solids-profile multipliers
Waste-dependent horizon for dynamic relaxation
Scaled component-equation acceptance residual
Coordinatewise root error, absolute error, and bias
Coefficient of determination for a plant-response coordinate
Holdout-range normalization of a location-quality error
Operating-control normalization to the unit interval
Common center and displaced starts for the multistart comparison
Route-specific water-quality objective scales
Difference between route-native and reference-model objectives
Reference-model objective difference between optimization routes
Normalized operating-control differences and their summaries
Percentage removal of a reported water-quality quantity
'@ -split '\r?\n'
$encoding = New-Object System.Text.UTF8Encoding($false)

function Remove-EquationNames([string]$Text) {
    [regex]::Replace($Text, '\\equationname\{[^{}]*\}\r?\n[ \t]*', '')
}

function Get-EquationRows([string]$Body, [string]$Environment) {
    if ($Environment -eq 'equation') {
        [pscustomobject]@{ Text = $Body; Separator = ''; Numbered = $true }
        return
    }
    $depth = 0
    $braces = 0
    $start = 0
    $tokens = [regex]::Matches($Body, '\\begin\{[^}]+\}|\\end\{[^}]+\}|\\\\(?:\[[^\]]*\])?|\\[{}]|[{}]')
    foreach ($token in $tokens) {
        if ($token.Value.StartsWith('\begin')) { $depth++; continue }
        if ($token.Value.StartsWith('\end')) { $depth--; continue }
        if ($token.Value -eq '{') { $braces++; continue }
        if ($token.Value -eq '}') { $braces--; continue }
        if ($token.Value.StartsWith('\\') -and $depth -eq 0 -and $braces -eq 0) {
            $text = $Body.Substring($start, $token.Index - $start)
            [pscustomobject]@{ Text = $text; Separator = $token.Value; Numbered = $text -notmatch '\\(?:notag|nonumber)\b' }
            $start = $token.Index + $token.Length
        }
    }
    $text = $Body.Substring($start)
    if ($text.Trim()) {
        [pscustomobject]@{ Text = $text; Separator = ''; Numbered = $text -notmatch '\\(?:notag|nonumber)\b' }
    } elseif ($text) {
        [pscustomobject]@{ Text = $text; Separator = ''; Numbered = $false }
    }
}

$pending = @()
foreach ($chapter in Get-ChildItem (Join-Path $root 'article/chapters/0[3-6]_*.tex') | Where-Object { $_.Name.Substring(0, 2) -in $Chapters } | Sort-Object Name) {
    $chapterId = $chapter.Name.Substring(0, 2)
    $original = [System.IO.File]::ReadAllText($chapter.FullName)
    $source = Remove-EquationNames $original
    $newline = if ($source.Contains("`r`n")) { "`r`n" } else { "`n" }
    $output = New-Object System.Text.StringBuilder
    $start = 0
    $number = 0
    $environments = [regex]::Matches($source, '(?s)\\begin\{(equation|align|gather|flalign|alignat)\}(.*?)\\end\{\1\}')
    foreach ($environment in $environments) {
        [void]$output.Append($source.Substring($start, $environment.Groups[2].Index - $start))
        foreach ($row in Get-EquationRows $environment.Groups[2].Value $environment.Groups[1].Value) {
            $text = $row.Text
            if ($row.Numbered) {
                $number++
                if ($Apply) {
                    if (-not $titles.ContainsKey($chapterId) -or $number -gt $titles[$chapterId].Count) { throw "Missing title for $chapterId.$number" }
                    $prefix = [regex]::Match($text, '^\s*').Value
                    $indent = [regex]::Match($prefix, '[ \t]*$').Value
                    $text = $prefix + '\equationname{' + $titles[$chapterId][$number - 1] + '}' + $newline + $indent + $text.Substring($prefix.Length)
                } else {
                    $summary = [regex]::Replace($text, '\s+', ' ').Trim()
                    Write-Output ($chapterId.TrimStart('0') + '.' + $number + ' | ' + $summary)
                }
            }
            [void]$output.Append($text + $row.Separator)
        }
        $start = $environment.Groups[2].Index + $environment.Groups[2].Length
    }
    [void]$output.Append($source.Substring($start))
    if ($number -ne $expected[$chapterId]) { throw "Equation count mismatch for $chapterId, found $number" }
    $revised = $output.ToString()
    if ((Remove-EquationNames $revised) -cne $source) { throw "Mathematical content changed in $($chapter.Name)" }
    if ($Apply -and $titles[$chapterId].Count -ne $number) { throw "Unused titles for $chapterId" }
    $pending += [pscustomobject]@{ Path = $chapter.FullName; Text = $revised; Count = $number }
}
if ($pending.Count -ne $Chapters.Count) { throw 'The selected chapter identifiers must match the source filenames.' }
if ($Apply) {
    foreach ($chapter in $pending) { [System.IO.File]::WriteAllText($chapter.Path, $chapter.Text, $encoding) }
    Write-Output ('Applied equation descriptions to ' + (($pending | Measure-Object Count -Sum).Sum) + ' numbered equations without changing mathematical content.')
}