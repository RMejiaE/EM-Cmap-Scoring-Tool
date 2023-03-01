# Naming protocol
The following document describes the rules for naming variables and functions, as well as some general good programming practices for presenting them in the code.

# General rules:
-	All variables will be listed at the top of the program file, after the imports.
-	Instances will be listed at the top, after variables.
-	Functions prototypes will be listed at the top, after instances.
## Variables and Functions:
Variables will follow the template presented below following table 1 rules:

*vScopeType_name*
 
 ### Table 1: Identifiers for variables names
| ID	| Scope |	Type |	Underscore |	name |
|:-----:|:-------:|------|:-------------:|-------|
|  v | Loc |	L(ist) |	_	| alpha |
|   |	Glo	| T(uple) |	_	| bravo |
|   |		| C(har) |	_	| charlie |
|   |		| F(loat) |	_ |	delta |
|   |		| I(nt) |	_ |	echo |

**e.g., vGloL_concept**

Functions will follow the template presented below:

*fScopeType_name()*

**e.g., f_inputfiles()**

## Instances and Objects
Instances will follow the template presented below:

*iClass_name*

**e.g., iLabel_frame, iLabel_rootconcept, iCheckbox_trad**

Objects will follow the template presented below:

*oClass_name*
