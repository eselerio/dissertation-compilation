from pathlib import Path

root=Path(__file__).resolve().parents[1]
p=root/'article/chapters/03_reactor_foundations.tex'
t=p.read_text(encoding='utf8')
biology=r'''
\section{Biological meaning of the component transformations}

\subsection{Electron donors, electron acceptors, and biomass}

Microorganisms use part of a substrate to obtain energy and another part to form cellular material. An electron donor supplies electrons in an oxidation reaction. An electron acceptor receives them in a reduction reaction. Under aerobic conditions, organic material can serve as the donor and oxygen as the acceptor. Under anoxic conditions, some organisms use nitrate or nitrite instead of oxygen. Naming the donor and acceptor helps explain why the same organic substrate can support different treatment pathways \citep{Narayanan2021,Preena2021}.

The carbon source and the energy source describe different properties. Heterotrophic biomass uses organic carbon to form cells. Chemolithoautotrophic nitrifying biomass obtains energy from inorganic nitrogen oxidation and uses inorganic carbon for cell synthesis. Its growth is therefore not simply another form of organic-substrate removal. The separate biomass coordinates in the adopted model retain this distinction \citep{Henze2006,Guerrero2011}. Complete ammonia oxidation can also occur within one microbial organism \citep{VanKessel2015}. That biological observation does not replace the separate ammonium- and nitrite-oxidation processes in the adopted model.

An idealized organic unit, $\mathrm{CH_2O}$, illustrates oxidation without assigning one chemical formula to all wastewater organic matter. Its complete aerobic oxidation is
\begin{equation}
\mathrm{CH_2O}+\mathrm{O_2}\longrightarrow\mathrm{CO_2}+\mathrm{H_2O}.
\label{eq:teaching_carbon_oxidation}
\end{equation}
Both sides contain one carbon atom, two hydrogen atoms, and three oxygen atoms. Using approximate molar masses of 30 g mol$^{-1}$ for the organic unit and 32 g mol$^{-1}$ for oxygen gives $32/30=1.067$ g oxygen per g of this idealized material. A hypothetical 30 g of this material would require 32 g oxygen for complete oxidation. The example explains the oxygen-demand basis of organic components. It does not prescribe the oxygen demand of an arbitrary wastewater mixture.

Cell synthesis changes that accounting because part of the carbon and nitrogen enters biomass. The empirical formula $\mathrm{C_5H_7O_2N}$ is a useful teaching representation of biomass composition, as discussed in the assimilation study of \citet{Hoover1952}. It describes an average composition rather than a single molecular species. For example, an idealized complete oxidation of this biomass with nitrogen released as ammonium can be written as
\begin{equation}
\mathrm{C_5H_7O_2N}+5\mathrm{O_2}+\mathrm{H^+}
\longrightarrow5\mathrm{CO_2}+\mathrm{NH_4^+}+2\mathrm{H_2O}.
\label{eq:teaching_biomass_oxidation}
\end{equation}
The carbon, hydrogen, oxygen, and nitrogen counts are respectively 5, 8, 12, and 1 on each side. The net charge is $+1$ on each side. Five moles of oxygen correspond to 160 g, while the empirical biomass unit has an approximate mass of 113 g. The ratio is therefore about 1.416 g oxygen per g of this idealized biomass. These calculations distinguish dry biomass mass from biomass COD. The adopted model uses its specified yields, constituent contents, and lysis processes rather than substituting these teaching reactions for its stoichiometric entries.

\subsection{Nitrogen transformations and their oxygen requirements}

Separating nitrification into two steps makes the oxygen demand and the nitrite intermediate visible. Ignoring cell synthesis for this teaching calculation, the ammonium-oxidation and nitrite-oxidation reactions are
\begin{align}
\mathrm{NH_4^+}+\tfrac32\mathrm{O_2}
&\longrightarrow\mathrm{NO_2^-}+2\mathrm{H^+}+\mathrm{H_2O},
\label{eq:teaching_ammonium_oxidation}\\
\mathrm{NO_2^-}+\tfrac12\mathrm{O_2}
&\longrightarrow\mathrm{NO_3^-}.
\label{eq:teaching_nitrite_oxidation}
\end{align}
The first reaction preserves one nitrogen atom, four hydrogen atoms, and three oxygen atoms. Its right-hand charge is $-1+2=+1$, which equals its left-hand charge. The second reaction preserves one nitrogen atom, three oxygen atoms, and a net charge of $-1$. Adding the reactions and cancelling the intermediate nitrite gives
\begin{equation}
\mathrm{NH_4^+}+2\mathrm{O_2}
\longrightarrow\mathrm{NO_3^-}+2\mathrm{H^+}+\mathrm{H_2O}.
\label{eq:teaching_overall_nitrification}
\end{equation}

Each mole of nitrogen has an approximate mass of 14 g. The first step requires $1.5(32)/14=3.43$ g oxygen per g nitrogen. The second requires $0.5(32)/14=1.14$ g oxygen per g nitrogen. Their sum is 4.57 g oxygen per g nitrogen. A hypothetical conversion of 10 g ammonium nitrogen to nitrate would therefore require about 45.7 g oxygen under these idealized assumptions. Actual process demand also depends on biomass synthesis and the adopted yields. The hydrogen ions in the first step explain why nitrification also draws on the buffering capacity represented by alkalinity \citep{Guerrero2011,Henze2006}.

Denitrification uses oxidized nitrogen as an electron acceptor and can convert it to dinitrogen. With $\mathrm{CH_2O}$ as the illustrative donor and with cell synthesis omitted, two balanced net reactions are
\begin{align}
4\mathrm{NO_3^-}+5\mathrm{CH_2O}+4\mathrm{H^+}
&\longrightarrow2\mathrm{N_2}+5\mathrm{CO_2}+7\mathrm{H_2O},
\label{eq:teaching_nitrate_denitrification}\\
4\mathrm{NO_2^-}+3\mathrm{CH_2O}+4\mathrm{H^+}
&\longrightarrow2\mathrm{N_2}+3\mathrm{CO_2}+5\mathrm{H_2O}.
\label{eq:teaching_nitrite_denitrification}
\end{align}
For the nitrate reaction, both sides contain four nitrogen atoms, five carbon atoms, fourteen hydrogen atoms, and seventeen oxygen atoms. Its left-hand charge is $-4+4=0$, matching the uncharged products. The nitrite reaction can be checked in the same way. The donor requirements are $5/4$ and $3/4$ moles of the illustrative organic unit per mole of nitrogen. This difference explains why the pathway through nitrite can require less organic donor than the pathway through nitrate under the same simplified assumptions. Carbon supply and donor identity also affect denitrification kinetics, as reviewed by \citet{Lu2014}. A stoichiometric requirement alone does not establish a reaction rate.

Anaerobic ammonium oxidation provides a different nitrogen pathway. An idealized net reaction that omits biomass synthesis and minor products is
\begin{equation}
\mathrm{NH_4^+}+\mathrm{NO_2^-}
\longrightarrow\mathrm{N_2}+2\mathrm{H_2O}.
\label{eq:teaching_anammox}
\end{equation}
It preserves two nitrogen atoms, four hydrogen atoms, two oxygen atoms, and zero net charge. It couples ammonium and nitrite without an organic electron donor in this idealized balance. The cultivation work of \citet{Strous1999} and the pathway studies of \citet{Dietl2015,Maalcke2016} explain why it differs biologically from ordinary heterotrophic denitrification. Its application requires its own organisms and operating conditions \citep{Vandekerckhove2018,Xie2021,WinklerStraka2019}. It is included here to clarify the boundary of the nitrogen discussion. It is not an additional process in the adopted 20-component, 28-process reactor model.

\subsection{From elemental accounting to the adopted state basis}

The teaching reactions permit direct checks of atom counts and charge because every displayed species has a chemical formula. An activated sludge state instead combines oxygen-demand equivalents, nitrogen mass, phosphorus mass, solids mass, and alkalinity. A biomass coordinate in g COD m$^{-3}$ cannot be added directly to a nitrogen coordinate in g N m$^{-3}$ to obtain a material total. Its nitrogen-content coefficient must first convert its contribution to the nitrogen basis.

\citet{TakacsVanrolleghem2006} explain the distinction between balances on lumped wastewater components and complete elemental accounting. A full elemental balance may require water, carbon dioxide, gas exchange, and other species outside a particular activated sludge state. The mass conservation conditions in this dissertation are established from the adopted stoichiometric matrix and the declared flow and transfer boundary. They certify the quantities represented by that model. They do not imply that every unrepresented chemical species or external flux has been measured. The derivation below identifies the precise quantities that can be imposed without adding an unsupported physical condition.

'''
anchor=r'\section{Process transformations and their rates}'
assert anchor in t
t=t.replace(anchor,biology+anchor,1)
t=t.replace('Every consistent with mass conservation component change','Every component change consistent with mass conservation')
t=t.replace('from a inventory used for mass conservation','from an inventory used for mass conservation')
t=t.replace('An invariant-preserving change','A change satisfying mass conservation')
t=t.replace('Every change preserving the weighted sum','Every change satisfying mass conservation for the weighted sum')
strict='A strictly positive coordinate satisfies $c_j>0$, whereas non-negativity permits $c_j=0$. The distinction matters when a logarithm or a reciprocal is evaluated. Such an operation can require a strictly positive argument even though a physical concentration may legitimately be zero.'
anchor='Subscripts identify the coordinate being discussed.'
t=t.replace(anchor,strict+'\n\n'+anchor,1)
spatial=r'''
\section{Mixing and spatial transport as model boundaries}

The preceding reactor balance assumes a single mixed concentration for each component in a reactor. This assumption removes spatial coordinates from that reactor state. It is a modeling decision rather than a claim that every treatment unit is uniform. Biofilms, trickling filters, and aerated vessels with incomplete mixing can have concentration gradients and transport limitations \citep{Wik2003,Zhang1994,SadinoRiquelme2020}. These effects provide useful context for interpreting the scope of a mixed-reactor surrogate.

A small spatial control volume illustrates the additional accounting. For one component, let $V$ be its fixed volume and $\bar c$ its average concentration. Let $F_{\rm adv,in}$ and $F_{\rm adv,out}$ be advective mass flow rates. Let $F_{\rm diff,in}$ and $F_{\rm diff,out}$ be diffusive mass flow rates. The finite-volume balance is
\begin{equation}
V\frac{\mathrm d\bar c}{\mathrm dt}
=F_{\rm adv,in}-F_{\rm adv,out}
+F_{\rm diff,in}-F_{\rm diff,out}+Vr.
\label{eq:teaching_spatial_control_volume}
\end{equation}
The symbol $r$ is the net reaction production rate per unit volume. It can be negative when the component is consumed. Every term on the right has units of component mass per time. For a hypothetical volume of 2 m$^3$, advective inflow and outflow of 5 and 3 g d$^{-1}$, diffusive inflow and outflow of 2 and 0 g d$^{-1}$, and total reaction consumption of 3 g d$^{-1}$, the accumulation is $5-3+2-0-3=1$ g d$^{-1}$. Dividing by the volume gives $\mathrm d\bar c/\mathrm dt=0.5$ g m$^{-3}$ d$^{-1}$. This calculation shows why the reaction term alone cannot determine a local concentration change.

In a one-dimensional domain with coordinate $z$, the advective flux is $v c$ and the diffusive flux is $-D_z\partial c/\partial z$. Here $v$ is the velocity and $D_z$ is a dispersion or diffusion coefficient. Dividing the balance of a slice by its volume and taking the limit as its thickness decreases gives
\begin{equation}
\frac{\partial c_j}{\partial t}
=-\frac{\partial(v c_j)}{\partial z}
+\frac{\partial}{\partial z}
\left(D_z\frac{\partial c_j}{\partial z}\right)
+\sum_{p=1}^{n_p}\nu_{pj}\rho_p+s_j.
\label{eq:teaching_spatial_balance}
\end{equation}
The term $s_j$ represents a specified external source per unit volume. The first two terms express spatial transport. The summation is the same component-by-component reaction accounting used in the mixed reactor. Boundary conditions specify how material enters and leaves the spatial domain. An invariant weighted sum cancels compatible reaction terms, but the transport and external-source terms still remain in its balance.

This spatial formulation explains how the theoretical ideas can extend to other treatment representations. It is not an additional spatial reactor in the present study. Chapter~\ref{ch:plant} uses mixed reactor stages and a layered clarifier. The stages represent sequential treatment conditions, while the clarifier layers represent solids transport and inventory. Their distinct boundaries must be respected when mass conservation is imposed.
'''
assert spatial.strip() not in t
t += '\n'+spatial
p.write_text(t,encoding='utf8')

# The relaxation is a theoretical comparison, not an adopted replacement for
# the fixed-topology plant optimization.
p=root/'article/chapters/06_connected_plant.tex'
t=p.read_text(encoding='utf8')
relaxation=r'''
\section{Bounded products and the limits of a convex relaxation}

Flow and concentration products help explain why process optimization remains nonlinear even when a surrogate is linear in its fitted coefficients. A bounded product provides a simple example. Let $x_L\leq x\leq x_U$, $y_L\leq y\leq y_U$, and let $z$ represent the product $xy$. The four products
\[
(x-x_L)(y-y_L),\quad (x_U-x)(y_U-y),\quad
(x_U-x)(y-y_L),\quad (x-x_L)(y_U-y)
\]
are non-negative. Expanding the first gives $xy-x_Ly-y_Lx+x_Ly_L\geq0$. Replacing $xy$ by $z$ gives one lower bound on $z$. Expanding the other three products gives the remaining bounds. Together they form the McCormick relaxation \citep{McCormick1976}
\begin{equation}
\begin{aligned}
z&\geq x_Ly+y_Lx-x_Ly_L,\\
z&\geq x_Uy+y_Ux-x_Uy_U,\\
z&\leq x_Uy+y_Lx-x_Uy_L,\\
z&\leq x_Ly+y_Ux-x_Ly_U.
\end{aligned}
\label{eq:teaching_mccormick_relaxation}
\end{equation}
The four inequalities are linear in the variables $x$, $y$, and $z$. Every exact product within the stated bounds satisfies them. Their intersection nevertheless permits points that do not satisfy $z=xy$.

For a hypothetical pair with $0\leq x,y\leq1$, the bounds become $z\geq0$, $z\geq x+y-1$, $z\leq x$, and $z\leq y$. At $x=y=0.5$, they permit $0\leq z\leq0.5$. The exact product is only $z=0.25$. A favorable objective obtained at another permitted value of $z$ is therefore not, by itself, an attainable process response. Tighter variable bounds can improve the relaxation, but they do not generally replace the exact product relation. Process-network optimization uses this distinction when constructing bounds and assessing solutions \citep{RubioCastro2010,YangNetwork2014}.

This example separates a convex relaxation from the physical projection used here. The relaxation enlarges a nonlinear feasible set to obtain an optimization bound. The projection selects a response satisfying the declared mass conservation and non-negativity conditions near a predicted response. Neither operation alone proves that a control vector is a global optimum of the full mechanistic plant. The present fixed-configuration plant retains the surrogate-assisted and direct mechanistic searches described below. It does not substitute a mixed-integer network-design formulation for those searches.

'''
anchor=r'\section{A direct mechanistic comparator}'
assert anchor in t
t=t.replace(anchor,relaxation+anchor,1)
t=t.replace('Positivity of the exponential','Strict positivity of the exponential')
t=t.replace(r'Positivity of Equation~\eqref{eq:plant_log_prediction}',r'Strict positivity of Equation~\eqref{eq:plant_log_prediction}')
p.write_text(t,encoding='utf8')
