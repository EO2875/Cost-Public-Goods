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
/* Additional data:
note: lifeExp popWB safewater hygiene measles electric secondaryschool from World Bank WDI;
note: parcomp xropen xrcomp  democ autoc polity polity2 from Polity Project;
note: dd_Przeworski is Przeworksi democracy measure;
note: gwf_demo gwf_demo gwf_party gwf_military gwf_monarchy gwf_personal gwf_nonautocracy are Geddes et al institutional measures;
note: food from FAOSTAT_data_9-2-2020 Average dietary energy supply adequacy (percent) (3-year average);
note: transparencyindex for Hollyer, Rosendorff and Vreeland ;
note: pressRestrict if Freedom House restriction on press freedom;
note: cpiscore is  Corruption Perception index from Tranparency International;
note: pop is from Maddison population data; */

/********************************************************************************/
/************************ Construct Institutional Measures **********************/
/********************************************************************************/
use "NewWmeasure-full.dta", clear;

/********************************************************************************/
/************************ Construct New W measure *******************************/
/********************************************************************************/
sort ccode year;

/* Make Other Institutional Variables */
gen demaut =(polity2+10)/20;
label var demaut "Polity: (democracy score - autocracy score +10)/20";
rename demaut normpolity;
/* Selectorate */
gen S_old=(LegislativeSelection)/2  ;
label var S_old "Selectorate size";
/* Old Coalition Size: W  */
gen W_old=0;
replace W_old=W_old+1 if (xrcomp>=2);
replace W_old=W_old+1 if (xropen>2);
replace W_old=W_old+1 if parcomp==5;
/* Banks regime type recorded only thru 2016: uopdate thru 2018 assuming no change */
replace RegType =RegType[_n-1] if year==2017 & year[_n-1]==2016;
replace RegType =RegType[_n-1] if year==2018 & year[_n-1]==2017;
replace W_old=W_old + 1 if (RegType~=. & RegType~=2 & RegType~=3);
replace W_old=W_old/4;
label var W_old  " Winning Coalition size (old)";

gen Democracy6=polity2>=6; replace Democracy6=. if polity2==.;
gen Democracy10=polity2==10; replace Democracy10=. if polity2==.;
 #delimit;
gen DemAnoAuto = 0 if polity2~=. ;
replace DemAnoAuto = 1 if polity2~=. &polity2>=6;
replace DemAnoAuto = -1 if polity2~=. &polity2<= -6;
#delimit; gen S=S_old;
carryforward v2x_suffr, gen(Suffrage);
replace S=Suffrage;
/*** new code **/;
replace S=log(S+1);
rename v2regsupgroupssize sup;
sum sup; gen support= (sup-r(min))/(r(max)-r(min)); label var support "Support";

rename Democracy6 Dem6;
rename dd_Przeworski Przeworski;

/***** Non- V-Dem Variables*****/
rename lifeExp LifeExpect;
rename  measles Vaccination ;
rename safewater CleanWater;
rename hygiene Hygiene ;
rename food FoodConsumption;
rename electric ElectricAccess;
rename   secondaryschool SecondarySchool;
rename  transparencyindex Transparencyindex;
rename  pressRestrict PressFreedom  ;
rename cpiscore CorruptionTI;

export delimited
    country_name ccode year
    support
    W_old normpolity Dem6 e_boix_regime Przeworski
    gwf_party gwf_military gwf_monarchy  gwf_personal gwf_demo
    LifeExpect Vaccination CleanWater Hygiene FoodConsumption ElectricAccess
    SecondarySchool Transparencyindex PressFreedom CorruptionTI
    /* HealthExpend EducExpend */
    using "bdm-extras.csv" ;

