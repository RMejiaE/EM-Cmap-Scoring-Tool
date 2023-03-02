# ⚠️ Naming protocol
The following document describes the rules for naming variables and functions, as well as some general good programming practices for presenting them in the code.

# 📝 General rules:
-	All variables will be listed at the top of the program file, after the imports.
-	Instances will be listed at the top, after variables.
-	Functions prototypes will be listed at the top, after instances.
## Variables and Functions:
Variables will follow the template presented below following table 1 rules:

*vScopeType_name*
 
 ### Table 1: Identifiers for variables names
| ID	| Scope |	Type |	Underscore |	name |
|:-----:|:-------:|:------:|:-------------:|-------|
|  v(ariable) | Loc |	L(ist) |	_	| var_1 |
|   |	Glo	| T(uple) |	_	| var_2 |
|   |	Ext	| C(har) |	_	| var_3 |
|   |		| F(loat) |	_ |	var_4 |
|   |		| I(nt) |	_ |	var_5 |
|   |		| D(ictionary) |	_ |	var_6 |

**e.g., vGloL_concept**

Functions will follow the template presented below:

*fscope_name()*

 ### Table 2: Identifiers for function names
| ID	| Scope |	Underscore |	name |
|:-----:|:-------:|:-------------:|-------|
|  f(unction) | Loc |	_	| function_1 |
|   |	Ext |	_	| function_2 |

**e.g., fLoc_inputfiles()**

## Instances and Objects
Instances will follow the template presented below:

*iClass_name*

**e.g., iLabel_frame, iLabel_rootconcept, iCheckbox_trad**

Objects will follow the template presented below:

*oClass_name*
