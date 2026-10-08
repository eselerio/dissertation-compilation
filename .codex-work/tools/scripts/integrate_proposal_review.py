from pathlib import Path

root=Path(__file__).resolve().parents[3]
path=root/'article/chapters/02_integrated_literature.tex'
text=path.read_text(encoding='utf8')
blocks=[]
def insert(anchor,content): blocks.append((anchor,content.strip()+'\n\n'))

insert(r'\section{Why treatment analysis calls for surrogate models}',r'''
\section{Development and calibration of activated sludge models}

The history of activated sludge modeling explains why a component response has an explicit scientific meaning. \citet{Marais1976} develop steady-state treatment relationships that connect biomass, substrate, and operating conditions. \citet{Dold1981} extend the representation toward a general process model. These works establish a distinction between an observed effluent total and the internal quantities used to calculate that total. A surrogate intended for component prediction inherits that distinction.

\citet{Henze1987} describe a general single-sludge formulation associated with Activated Sludge Model No.\ 1 (ASM1). Its process structure separates substrate use, biomass growth, decay, and nitrogen transformations. \citet{Gujer1999} develop Activated Sludge Model No.\ 3 (ASM3) with an explicit role for intracellular storage. The choice between these representations changes which intermediate states are available for prediction. A statistical model cannot infer a uniquely defined hidden storage state unless the supervised representation defines that state.

Nutrient-removal models extend the same principle. \citet{Barker1997} present a general biological nutrient-removal model, while \citet{Hu2007} develop a kinetic treatment of the linked processes. The phosphorus-removal formulation of \citet{Henze1999} adds another established component and process description. These sources support joint treatment of carbon, nitrogen, and phosphorus. They also show why a model name does not make every parameter or microbial pathway interchangeable.

\citet{Rieger2001} connect biological phosphorus removal to the storage-based formulation. \citet{Fall2015} modify an activated sludge model for low solids production. These contributions identify different purposes for model extension. Adding a process or changing a yield can alter the component relationships and the corresponding mass conservation conditions. An invariant operator must therefore be derived from the adopted stoichiometric matrix rather than borrowed from a model with similar names.

Model development has a practical history as well as a mathematical one. \citet{VanLoosdrecht2015} review the development and use of ASM1 over twenty-five years. \citet{Hauduc2013} examine the state of process knowledge, modeling concepts, and limitations. Their discussions support deliberate selection of a representation for a defined question. More states can describe additional mechanisms, but they also require additional information for calibration and assessment.

\citet{Petersen2003} review experimental designs for activated sludge calibration. \citet{Vanrolleghem1999} use respirometry to estimate model parameters and components. These studies connect a model quantity to the measurements that can support it. An oxygen-use observation can inform biological activity, but it is not a direct observation of every modeled component. The same issue arises when a surrogate is assessed against a few reported water quality measurements.

\citet{Meijer2004} examine the practical validation and calibration of a metabolic phosphorus-removal model. Their work distinguishes steady-state and dynamic information in testing a model. \citet{Nelson2009} analyze ASM1 mathematically. Together, these sources make clear that calibration, solution of the equations, and analysis of the resulting state are separate responsibilities. A good fit, a converged numerical solve, and an accepted physical state need not provide the same evidence.

The empirical biomass formula discussed by \citet{Hoover1952} supplies a useful historical example of constituent accounting. Biomass growth and decay redistribute organic matter and nitrogen, so a solids concentration cannot be treated as chemically empty material. \citet{TakacsVanrolleghem2006} examine elemental balances in activated sludge models and the role of omitted reaction products. Their contribution is especially relevant to projection. Mass conservation in an adopted lumped-component basis does not automatically establish complete elemental accounting for unrepresented water, carbon dioxide, or other boundary terms.

\section{Biological pathways and the boundaries of a model}

The functional role of a microorganism depends on both its energy source and its carbon source. Heterotrophic growth uses organic material, while nitrifying chemolithoautotrophs obtain energy from inorganic nitrogen transformations and use inorganic carbon for synthesis. \citet{Narayanan2019} review biological treatment and bioreactor design. \citet{Preena2021} review nitrification and denitrification in recirculating aquaculture. The latter setting differs from municipal activated sludge, but the distinction among electron donors, electron acceptors, and nitrogen forms remains useful.

Two-step nitrification separates ammonium oxidation from nitrite oxidation. It is an engineering representation of functional conversions rather than a universal rule about how many organisms perform them. \citet{VanKessel2015} establish complete nitrification within one microorganism. Their work explains why an explicit two-population model is a chosen process representation. It should not be interpreted as excluding every biological route that combines those functions.

\citet{Lu2014} review the microbial ecology of denitrification in biological wastewater treatment. Carbon availability, electron-acceptor conditions, and microbial populations jointly influence the nitrogen response. This supports retaining carbon and nitrogen components together when learning a surrogate. It also explains why the amount of reported nitrogen can change through conversion and separation even when the complete modeled nitrogen inventory satisfies mass conservation.

Anaerobic ammonium oxidation provides a different nitrogen pathway. \citet{Strous1998} study slowly growing anaerobic ammonium-oxidizing microorganisms. \citet{Dietl2015} investigate the hydrazine synthase complex, while \citet{Maalcke2016} examine the enzyme involved in nitrogen-gas production from hydrazine. These works clarify that a shared final nitrogen product does not make the underlying process identical to heterotrophic denitrification. The adopted reactor model does not contain an explicit anaerobic ammonium-oxidation population or its full kinetic pathway.

Temperature and treatment purpose create further boundaries. \citet{Vandekerckhove2018} investigate thermophilic nitrogen removal, and \citet{Xie2021} develop strategies for nitrogen conversion, recovery, and removal. \citet{WinklerStraka2019} review newer directions in biological nitrogen management. Their relevance is the need to identify which nitrogen transformation and engineering goal a model represents. A parameterized steady-state activated sludge surrogate does not acquire these additional capabilities through mass conservation and non-negativity alone.

\section{Suspended-growth and attached-growth treatment}

Suspended-growth and attached-growth systems organize biological activity differently. A completely mixed activated sludge reactor uses one bulk concentration vector for its control volume. A biofilm or packed treatment medium can contain spatial gradients and retained biomass at different locations. \citet{Wik2003} review trickling filters and biofilm modeling. \citet{Zhang1994} examine biofilm density, porosity, and pore structure. These contributions explain why transport and geometry can affect reaction rates even when the same nitrogen or organic-matter conversion is considered.

\citet{Machdar1997} develop a combined anaerobic and aerobic treatment setting for developing countries. \citet{Tawfik2006} examine combined anaerobic treatment and a down-flow sponge system. \citet{Tawfik2010} investigate the role of sponge volume in that downstream process. These studies connect treatment configuration and retained medium to the response being predicted. A medium volume or transport property is a different input from the hydraulic and aeration controls of a completely mixed reactor.

\citet{Mahmoud2010} study a naturally ventilated bio-tower for organic and nutrient treatment, and \citet{Mahmoud2011} examine a sponge reactor for municipal wastewater post-treatment. \citet{Hatamoto2018} relate sponge-reactor structure to process function and microbial communities. These contributions establish attached-growth treatment as a relevant engineering context. They do not supply additional evaluated cases for the present activated sludge benchmark.

\citet{Hellal2021} simulate a passively aerated biological filter, while \citet{Liang2021} model a three-stage biological trickling filter. \citet{Laine1999} examine dynamic nitrification in a low-loaded trickling filter. Their different configurations show why stage structure, spatial transport, and time dependence need to be identified before model responses are compared. A surrogate can be fast while approximating a different physical problem from the one intended.

Nutrient form also matters in these systems. \citet{Kasi2011} model dissolved organic nitrogen in a two-stage trickling filter, and \citet{Simsek2012} examine its fate. \citet{BressaniRibeiro2021} investigate inorganic carbon limitation during nitrogen conversions in sponge-bed treatment. These works connect prediction targets to constituent forms and growth requirements. They reinforce the need to retain the component basis rather than treating one measured nitrogen total as a complete process state.

\citet{DiezMontero2019} assess a trickling-filter upgrade for nutrient removal. \citet{Luan2023} examine nitrification and denitrification in a rotating self-aerated biofilm reactor. Both illustrate the engineering importance of configuration-specific process relationships. A statistical predictor trained for one hydraulic and biological arrangement requires new evidence before transfer to another.

The resource setting is also relevant. \citet{Tyagi2021} review the energy-saving motivation for sponge treatment, and \citet{Nasr2022} discuss its decentralized applications. \citet{Rapi2021} apply biological sponge treatment to palm oil mill effluent. These sources broaden the context of treatment selection while keeping the wastewater type explicit. Industrial and municipal influents can differ in their constituent distributions and treatment demands.

\citet{Mahmoud2018} consider post-treatment of anaerobic effluent containing a specific organic contaminant and heavy metals. Their setting illustrates a further limitation of a declared component model. The presence of metal-hydroxide and metal-phosphate coordinates does not make an activated sludge surrogate a general predictor of toxic-metal removal or every organic contaminant. The represented species and reactions determine that capability.

Transport modeling can join reaction kinetics with flow and diffusion. \citet{SadinoRiquelme2023} review how biological kinetics are integrated with computational fluid dynamics. The concern is the spatial location and transport of reacting material. The current standalone reactor and connected plant use their declared completely mixed stages and clarifier representation. Spatial treatment models provide a useful boundary comparison and a possible extension, rather than a replacement for those reference equations.
''')

insert(r'\section{Learning families and what each comparison can reveal}',r'''
\section{Prediction targets and information available to a decision}

Wastewater prediction studies often address a reported quantity rather than a complete mechanistic state. \citet{Ching2022} develop a soft sensor for five-day biochemical oxygen demand. \citet{ManavDemir2024} compare learning methods for nutrient-removal effluent parameters. These applications demonstrate the relevance of prediction to treatment monitoring. Their supervised target determines what an error score can establish. Agreement with one reported quantity does not establish mass conservation or non-negativity across the full component vector.

\citet{Ekinci2023} examine feature selection for sludge-production prediction. \citet{Wang2024} predict COD component parameters for activated sludge modeling. These contributions concern different output roles. A sludge production quantity, a wastewater fractionation parameter, and an effluent concentration are not interchangeable labels. The predictor inputs must also match the information available when each quantity is needed.

\citet{Poch1993} provide an observational treatment-plant dataset for classifying plant state and detecting faults. It contains measurements from different stages and performance quantities. A measurement can be a legitimate input for an operational diagnosis while remaining unavailable for prospective design or steady-state prediction at an untested setting. The dataset consequently helps explain information availability. It is not the training collection used for the current reactor or plant surrogates.

\citet{Caro2024} describe automated acquisition of simulator responses. Their contribution is relevant to the organization of paired model-generated observations. Such acquisition does not establish agreement with field measurements or eliminate the need for independent physical and numerical checks. The review of \citet{Sundui2021} places learning applications across biological wastewater tasks and similarly supports identifying the data source and intended output before comparing models.

Full-scale mechanistic applications provide complementary evidence. \citet{Wu2016} simulate and optimize a coking wastewater process with activated sludge models. \citet{SadriMoghaddam2021} address calibration of a full-scale plant model, and \citet{Jasim2020} develop a treatment-plant design model. These studies connect a model to a particular process setting. Their calibration does not remove the need to assess a surrogate separately on its sampled operating domain.

\citet{Szelag2022} examine nutrient removal and energy consumption under uncertainty. \citet{Nazif2023} formulate practical operating analysis with attention to influent characteristics. These contributions strengthen the decision context of model assessment. The operating response depends on the influent and parameter assumptions, so a selected decision should be evaluated at the stated conditions. Physical constraints do not remove every uncertainty in those conditions.
''')

insert(r'\section{Managing approximation during operating searches}',r'''
\section{Water networks and the distinction between topology and operation}

Water-network design separates the origins, combinations, and destinations of streams. A source supplies water with specified quantities and quality. A mixer combines compatible streams. A sink accepts water for a use or discharge requirement. \citet{Galan1998} optimize distributed wastewater treatment networks, and \citet{Galan1999} examine design and synthesis strategies for those networks. Their contribution concerns the choice of connected treatment and routing alternatives. The present connected plant uses a fixed topology and varies declared operating controls.

Regeneration and constituent-specific treatment complicate those choices. \citet{GuelliSouza2011} consider differentiated regeneration of contaminants in chemical-industry water reuse. \citet{YangNetwork2014} include wastewater regeneration models in network optimization. The treatment response influences which stream can reach which destination. These works show why a constant removal fraction can be an insufficient description when concentrations and operating conditions change.

Industry-specific applications make the boundary explicit. \citet{Gutterres2010} examine water reuse in tannery operations, \citet{Hansen2018} minimize water and wastewater in a petrochemical setting, and \citet{Xu2015} integrate a yeast-production water system. The application determines the relevant contaminants, unit operations, and water-use requirements. Their network methods are useful conceptual precedents, while their process states are not the activated sludge component targets.

\citet{RubioCastro2013} develop global optimization for property-based interplant water integration. Their result concerns the specified mathematical formulation and the conditions required by its optimization method. \citet{McCormick1976} provide convex underestimating relations for nonconvex factorable expressions. Such relations can support bounds on an optimization problem. They do not establish that a projected surrogate response satisfies every original nonlinear process equation.

\citet{Tosarkani2020} design a wastewater treatment network under uncertainty through a multiobjective robust formulation. \citet{Ye2019} use a hybrid particle-swarm approach for network planning. These contributions address uncertainty and search over a planning problem. The numerical route and stopping evidence must be distinguished from a global optimality certificate. A faster operating search in a fixed plant is a different contribution from selecting a globally optimal treatment network.

\citet{DamalerioRemoval2022} connect phosphorus-removal priorities with treatment-configuration and cost objectives. \citet{Selerio2022} develop regression-based optimization for urban water eutrophication abatement. Both connect response approximation to a declared decision purpose. Their relevance is the organized treatment of several engineering quantities. The current study retains a component-based activated sludge response, projection for mass conservation and non-negativity, and independent verification of selected controls.

\section{Approximation and the structure of an optimization claim}

\citet{KusiakWei2013} examine data-based optimization of the activated sludge process. Their contribution connects a learned response to operating selection. \citet{Niu2022} combine deep learning and multiobjective dynamic wastewater optimization. These studies illustrate different response representations and search settings. A steady-state operating comparison should identify its time basis and objective rather than treating all learning-based optimization as one task.

\citet{Jana2022} combine neural and support-vector regression methods in detergent-industry effluent optimization. \citet{Waqas2022} model membrane permeability for a rotating biological contactor, while \citet{Li2022} join response-surface and neural methods for membrane fabrication. These applications show how statistical approximation can enter an engineering search. They also show why evidence for one target cannot be transferred directly to a complete reactor component state.

\citet{Shojaei2021} discuss the optimization of conditions in wastewater degradation. \citet{Poh2016} review mechanistic and metaheuristic optimization in anaerobic digestion. The process models and decision variables differ from those of activated sludge, but the common issue is the relation between an inexpensive response calculation and a constrained operating choice. Model accuracy, search completeness, and the chosen priorities remain distinct.

\citet{JainKar2017} examine nonconvex optimization in machine learning. A model can be linear in its fitted coefficients while remaining nonlinear in its operating inputs. A convex projection at fixed inputs can also be embedded in a nonconvex outer search. This distinction is essential to the present contribution. Neither transparent regression terms nor an exactly solved projection alone establish a globally optimal operating decision.
''')

for anchor,content in blocks:
    if text.count(anchor)!=1: raise RuntimeError('Nonunique review anchor '+anchor)
    text=text.replace(anchor,content+anchor,1)
path.write_text(text,encoding='utf8')
print('Integrated proposal background in',len(blocks),'topic-linked literature sections.')
