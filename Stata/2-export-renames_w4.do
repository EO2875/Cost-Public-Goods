/********************************************************************/
/* Introducing New W measure and testing public/private goods */
/********************************************************************/
/* Bruce Bueno de Mesquita and Alastair Smith January 21, 2022 */
/* Paper forthcoming at Social Science Quarterly */
#delimit;
clear; set mem 50m;version 17;
cd "";/*insert your working directory here*/
pwd; frame change default;

/******** The main data sources: v-dem v11 downloaded March 18th 2021 */

/********************************************************************************/
/************************ Construct Institutional Measures **********************/
/********************************************************************************/
use "VDem_13.dta", clear;

/********************************************************************************/
/************************ Construct New W measure *******************************/
/********************************************************************************/
sort country_id year;
/**** Estimating W: higher values on these variables are better conditions that allow for a larger W****/
/* standarize variables so that mean=0 and sd=1*/
sum v2elembaut v2psoppaut v2psbars  ;

/*** Components for a restrictive regime **/
sort country_name;
by country_name: carryforward v2x_ex_hereditary, gen(Hereditary);
by country_name: carryforward v2x_ex_military, gen(Military);
by country_name: carryforward v2x_ex_party, gen(Party);

gen Big= Hereditary if Hereditary>=Party&Hereditary>=Military & Hereditary~=.;
replace Big=Party if Party>=Hereditary&Party>=Military&Party~=.;
replace Big=Military if Military>=Hereditary & Military>=Party & Military~=.;
gen biginst=(1-Big); sum biginst;
egen stdbiginst=std(biginst);

egen stdelembaut=std(v2elembaut);  /*** autonomy of election monitoring body***/
egen stdoppaut=std(v2psoppaut); /*** opposition parties' autonomy***/;
egen stdpsbars=std(v2psbars); /*** Barriers to political party partiipation***/;
gen extrapol= (stdbiginst~=. & (v2elembaut==. | v2psoppaut==.| v2psbars==.));

gen W4temp=(stdelembaut+stdoppaut+stdpsbars+stdbiginst)/4;
sum W4temp; /* standardize to 0,1 */
gen W4= (W4temp -r(min))/(r(max)-r(min));;

/**** Extropolate for those institutions with no electoral history ****/
/*** When there is zero electoral information (long established monarchies for instance) then set the electoral to the 1st percentile ***/;
sum v2elembaut, detail; replace v2elembaut=r(p1) if v2elembaut==.&biginst~=.;
sum v2psoppaut, detail; replace v2psoppaut=r(p1) if v2psoppaut==.&biginst~=.;
sum v2psbars, detail; replace v2psbars=r(p1) if v2psbars==.&biginst~=.;
egen Xstdelembaut=std(v2elembaut);  /*** autonomy of election monitoring body***/
egen Xstdoppaut=std(v2psoppaut); /*** opposition parties' autonomy***/;
egen Xstdpsbars=std(v2psbars); /*** Barriers to political party partiipation***/;

gen XW4temp=(Xstdelembaut+Xstdoppaut+Xstdpsbars+stdbiginst)/4;
sum XW4temp;
/* standardize to 0,1 */
gen XW4= (XW4temp -r(min))/(r(max)-r(min));

/******** XXXXXXXXXXXXXXXXXXXXXXXXXXXXX ***********/
/* Use extrapolated version */
rename W4 W4a; rename XW4 W4; rename XW4temp W4norm;
label var W4 "Measure of Winning Coalition Size based on 4 components of from V-Dem.";

drop Xstdpsbars Xstdoppaut Xstdelembaut W4temp extrapol stdpsbars stdoppaut stdelembaut stdbiginst biginst Big Party Military Hereditary;

/* Teorell and Lindberg 2019 */
global TL " v2x_ex_direlect v2x_ex_confidence v2x_ex_hereditary v2x_ex_military v2x_ex_party ";
sum $TL;
sort country_id year;

/******************************************************************/
/******************************************************************/
/******************** Organize Dependent Variables ****************/
/******************************************************************/
/******************************************************************/
sum v2excrptps;
gen normCorruption=1-(v2excrptps-r(min))/(r(max)-r(min));
sum v2peapspol;
gen normPublicGoods=(v2peapspol-r(min))/(r(max)-r(min));
gen ratiopublicprivate=(normPublicGoods)/(normPublicGoods+normCorruption);
gen logpop=log(e_wb_pop);
gen e_migdppcln=log(e_gdppc); /* Discontinued in V-Dem 13 */

/**** Analysis***/;
label var v2elfrfair "Free, Fair Elections";
label var v2exrescon "Exec. Respects Constitution";
label var v2x_clpol "Civil Liberties" /** High is good**/;
label var v2peapspol "Equal Access to Public Goods";
label var e_peinfmor "Infant Mortality";
label var e_pelifeex "Life Expectancy";
label var v2casurv "Campus Freedom";
label var v2xca_academ "Academic Freedom";
label var v2juhcind "Judicial Independence";
label var v2pehealth "Access to Health Care";
label var  e_fh_pr "Political Rights";
label var e_peaveduc  "Yrs Ed|Age>15";
label var e_migdppcln "log(income pc)";
label var v2x_rule "Rule of Law";
label var v2xcl_dmove "Free Movement";
label var v2xcl_slave "Free from Forced Labor";
label var v2xcl_prpty "Property Rights";
label var v2x_freexp "Free Expression";
gen PR_Up=(e_fh_pr-7)*-1;

global PublicGoods v2peapspol ratiopublicprivate v2dlencmps v2peapspol v2cltrnslw  v2dlcommon v2dlengage v2exrescon v2x_rule v2elfrfair v2xcl_dmove v2xcl_slave v2x_clpol PR_Up v2cltort v2clrelig v2juhcind v2jucorrdc v2xcl_prpty e_peinfmor v2casurv v2xca_academ v2pehealth v2x_freexp;

label var v2cltrnslw "Transparent Laws";
label var v2cltort "High No Torture";
label var v2jucorrdc "High No Judicial Corruption";
label var v2x_frassoc_thick "Freedom of Association";
label var v2dlcommon "Elite Deliberation Guided by Common Good";
label var v2dlengage "Public Deliberation Guided by Common Good";
label var v2dlencmps "Particularistic or Public Goods Spending";
label var v2excrptps "Corruption" /**High is good***/;
label var v2x_execorr "Executive Allows Corruption" /* "Media Censorship"; * High is bad***/;;
label var v2exthftps "Public Sector Theft" /**low is bad***/;
label var v2mecenefm "Media Censorship";  /** low is bad **/
label var v2jupack "Exec. Influences Court";
label var v2xpe_exlpol "Exclude Political Groups" /*High is bad***/;
label var v2xnp_client "Clientelism --Public $ for Pol Gain";
/****** Rename and recode variable to sensible names *****/
gen SlaveLabor = - v2xcl_slave;
gen Torture =-v2cltort;
gen JudgeCorrupt=-v2jucorrdc;
rename ratiopublicprivate GoodsRatio; rename v2elfrfair FreeElections;
rename v2exrescon RespectConstitution; rename v2x_clpol CivilLiberties;
rename v2peapspol AccessPubGoods; rename e_peinfmor InfantMortality;
rename v2casurv CampusFree; rename v2xca_academ AcademicFreedom;
rename v2juhcind JudicialIndep;
rename v2pehealth HealthCare; rename PR_Up PolRights;
rename v2x_rule RuleofLaw;
rename v2xcl_dmove FreeMovement; rename v2xcl_prpty PropertyRights;
rename v2x_freexp FreeExpression; rename v2cltrnslw TransparentLaws;
rename v2dlcommon EliteWantCommonGood; rename v2dlengage PublicWantCommonGood;
rename v2dlencmps PrivateorPublicGoods; rename normCorruption Corruption;
rename v2x_execorr ExecutiveCorrupt; rename v2exthftps PublicSectorTheft; replace PublicSectorTheft=-PublicSectorTheft;
rename v2mecenefm MediaCensored; rename v2jupack PackCourts;
replace PackCourts=-PackCourts;
rename v2clrelig ReligiousFreedom;
rename v2xnp_client Clientelism;
rename normPublicGoods PublicGoods;
replace v2clstown=-v2clstown;
rename v2clstown StateOwnsEconomy;

/* export delimited using "CY-DATA-V-Dem-13-renames-w4.csv", replace ; */

export delimited
    country_name country_id year
    W4 W4norm
    GoodsRatio
    FreeElections
    RespectConstitution
    CivilLiberties
    AccessPubGoods
    InfantMortality
    CampusFree
    AcademicFreedom
    JudicialIndep
    HealthCare
    PolRights
    RuleofLaw
    FreeMovement
    PropertyRights
    FreeExpression
    TransparentLaws
    EliteWantCommonGood
    PublicWantCommonGood
    PrivateorPublicGoods
    Corruption
    ExecutiveCorrupt
    PublicSectorTheft
    MediaCensored
    PackCourts
    ReligiousFreedom
    Clientelism
    PublicGoods
    StateOwnsEconomy
    SlaveLabor
    Torture
    JudgeCorrupt
    e_peaveduc
	e_wb_pop
	logpop
    e_gdppc
    e_migdppcln
    using "CY-DATA-V-Dem-13-renames-w4.csv", replace ;
