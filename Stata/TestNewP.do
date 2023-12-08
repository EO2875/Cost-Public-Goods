/*
ssc install carryforward
ssc install regen
ssc install ftools
ssc install reghdfe
ssc install ivreghdfe
ssc install estout, replace
*/

/********************************************************************/
/* Introducing New P measure and testing public/private goods */
/********************************************************************/
/* Jose Etienne Ortega Flores */
#delimit;
clear;
set mem 50m;
version 18;
capture mkdir output_9;
global store "output_9";
pwd;
frame change default;

import delimited "Full_Database.csv",case(preserve);

/************ Lists of Dependent Variables to be considered in groups ******/
#delimit;
global PublicGood PublicGoods GoodsRatio PrivateorPublicGoods  TransparentLaws EliteWantCommonGood PublicWantCommonGood
RespectConstitution RuleofLaw FreeElections FreeMovement SlaveLabor CivilLiberties PolRights Torture ReligiousFreedomv2clrelig
v2juhcind v2jucorrdc v2xcl_prpty e_peinfmor v2casurv v2xca_academ v2pehealth v2x_freexp;

/* very general set of public goods */
global EndogPublicGoods PublicGood  GoodsRatio PrivateorPublicGoods EliteWantCommonGood PublicWantCommonGood ;
global KeyPublicGoods TransparentLaws JudicialIndep FreeExpression ;
global EndogCorruptions Corruption ExecutiveCorrupt PublicSectorTheft Clientelism CorruptionTI ;
global KeyCorruptions StateOwnsEconomy JudgeCorrupt ;
global Freedoms RespectConstitution RuleofLaw FreeElections FreeMovement CivilLiberties PolRights ReligiousFreedom PropertyRights ;
global Abuse MediaCensored PackCourts Torture SlaveLabor ;
global EndogPublicEducation CampusFree AcademicFreedom /* EducExpend */ SecondarySchool ;
global OtherMeasures InfantMortality HealthCare LifeExpect Vaccination CleanWater Hygiene /* HealthExpend */ FoodConsumption ElectricAccess Transparency PressFreedom ;


capture log close;
log using "${store}/Log.smcl", replace;


/* Cost of Public Goods
  PWD_A,PWD_G,PWD_M
  wb_urbpop
  Elr,Epr,Err,Egr
  e_peaveduc
*/

/* Population-Weighted Density  */
gen l_pwd_a = log(PWD_A);
gen l_pwd_g = log(PWD_G);
gen l_pwd_m = log(PWD_M);

sum l_pwd_a ;
gen ln_pwd_a = (l_pwd_a - r(min))/(r(max) - r(min)) ;
sum l_pwd_g ;
gen ln_pwd_g = (l_pwd_g - r(min))/(r(max) - r(min)) ;
sum l_pwd_m ;
gen ln_pwd_m = (l_pwd_m - r(min))/(r(max) - r(min)) ;

/* Resemblances */
sum Elr ;
gen l_res_norm = (Elr - r(min))/(r(max) - r(min)) ;
sum Epr ;
gen p_res_norm = (Epr - r(min))/(r(max) - r(min)) ;
sum Err ;
gen r_res_norm = (Err - r(min))/(r(max) - r(min)) ;
sum Egr ;
gen g_res_norm = (Egr - r(min))/(r(max) - r(min)) ;

gen res = l_res_norm + p_res_norm + r_res_norm + g_res_norm ;
sum res ;
gen res_n = (res - r(min))/(r(max) - r(min)) ;

gen p1 = (g_res_norm + l_pwd_a) / 2 ;
gen p2 = (g_res_norm + wb_urbpop) / 2 ;
gen p3 = (p_res_norm + l_pwd_a) / 2 ;
gen p4 = (p_res_norm + wb_urbpop) / 2 ;
gen p5 = (g_res_norm + l_pwd_a + wb_urbpop) / 3;
gen p6 = (p_res_norm + g_res_norm + l_pwd_a + wb_urbpop) / 4 ;

/*
global dem_vars W4 support  W_old normpolity Dem6 e_boix_regime Przeworski
  gwf_party gwf_military gwf_monarchy  gwf_personal gwf_demo ;
global cost_vars
  ln_pwd_a ln_pwd_g ln_pwd_m 
  wb_urbpop
  l_res_norm p_res_norm r_res_norm g_res_norm
  e_peaveduc;
*/

/* global cost_vars ln_pwd_m wb_urbpop l_res_norm ; */
global dem_vars W4 ;
global cost_vars p1 p2 p3 p4 p5 p6;

set more off ;
/*
global titlelist ""Key Public Goods"  "Key Private Goods" "Fundamental Freedoms" "Abuse" "Health and Education" "Additional Measures" ";
*/
capture  file close csvfile2 ;


file open csvfile2 using "${store}/M3StatsComparisons.csv", write replace;

file write csvfile2 "Outcome,OutcomeCategory,Model,Stat,Result" _n ;

#delimit;
foreach outcat in EndogPublicGoods KeyPublicGoods KeyCorruptions Freedoms Abuse EndogPublicEducation OtherMeasures {;

  /********* Run analysis and collect appropriate stats **********/

  foreach outcome of global `outcat' {;
	/* ===================== M1 ===================== */
	foreach factr of global dem_vars {;
		reghdfe `outcome' `factr' e_migdppcln logpop , a(ccode year) resid vce(clu ccode) ;
		mat bb_w = e(b) ;
		mat eV_w = e(V) ;
		/*
		capture drop Wsm${m} ;
		capture capture drop Wsm${m}_2;
		predict Wsm${m},res;
		gen Wsm${m}_2=Wsm${m}^2;
		*/
		/* scalar rsq${dem}${cost}= e(r2) ;
		local rsq${dem}${cost} : display %6.3f scalar(rsq${m}) ; */
		estat ic ;
		mat aicm = r(S) ;
		/* scalar aicnw`factr' =aicm[1,5] ; */
		scalar aicnw`factr' =-2*e(ll)+ 2 * (e(df_m)+e(df_a)+1)  + 2*(e(df_m)+e(df_a)+1) *(e(df_m)+e(df_a)+2) /(e(N)-(e(df_m)+e(df_a)+1)-1) ;
		scalar bicnw`factr' = -2*e(ll)+ log(e(N)) * (e(df_m)+e(df_a)+1) ;
		local aicw`factr' : display %10.2f scalar(aicnw`factr') ;
		local bicw`factr' : display %10.2f scalar(bicnw`factr') ;
		local betaw`factr' : display %10.2f scalar(bb_w[1,1]) ;
		local tstatw`factr' : display %10.2f scalar(bb_w[1,1])/sqrt(eV_w[1,1]) ;
		local loglike`factr' : display %10.2f scalar(aicm[1, 3]) ;

		file write csvfile2 `"`outcome',`outcat',`factr',betaw,`betaw`factr''"' _n ;
		file write csvfile2 `"`outcome',`outcat',`factr',tstatw,`tstatw`factr''"' _n ;
		file write csvfile2 `"`outcome',`outcat',`factr',AIC,`aicw`factr''"' _n ;
		file write csvfile2 `"`outcome',`outcat',`factr',BIC,`bicw`factr''"' _n ;
		/* file write csvfile `"`outcome',`outcat',`factr',Vuong,`twald`dem'`cost''"' _n ; */
		file write csvfile2 `"`outcome',`outcat',`factr',loglike,`loglike`factr''"' _n ;
    };
	/* ===================== M2 ===================== */
	foreach factr of global cost_vars {;
		reghdfe `outcome' `factr' e_migdppcln logpop , a(ccode year) resid vce(clu ccode) ;
		mat bb_w = e(b) ;
		mat eV_w = e(V) ;
		/*
		capture drop Wsm${m} ;
		capture capture drop Wsm${m}_2;
		predict Wsm${m},res;
		gen Wsm${m}_2=Wsm${m}^2;
		*/
		/* scalar rsq${dem}${cost}= e(r2) ;
		local rsq${dem}${cost} : display %6.3f scalar(rsq${m}) ; */
		estat ic ;
		mat aicm = r(S) ;
		/* scalar aicnw`factr' =aicm[1,5] ; */
		scalar aicnw`factr' =-2*e(ll)+ 2 * (e(df_m)+e(df_a)+1)  + 2*(e(df_m)+e(df_a)+1) *(e(df_m)+e(df_a)+2) /(e(N)-(e(df_m)+e(df_a)+1)-1) ;
		scalar bicnw`factr' = -2*e(ll)+ log(e(N)) * (e(df_m)+e(df_a)+1) ;
		local aicw`factr' : display %10.2f scalar(aicnw`factr') ;
		local bicw`factr' : display %10.2f scalar(bicnw`factr') ;
		local betaw`factr' : display %10.2f scalar(bb_w[1,1]) ;
		local tstatw`factr' : display %10.2f scalar(bb_w[1,1])/sqrt(eV_w[1,1]) ;
		local loglike`factr' : display %10.2f scalar(aicm[1, 3]) ;

		file write csvfile2 `"`outcome',`outcat',`factr',betap,`betaw`factr''"' _n ;
		file write csvfile2 `"`outcome',`outcat',`factr',tstatp,`tstatw`factr''"' _n ;
		file write csvfile2 `"`outcome',`outcat',`factr',AIC,`aicw`factr''"' _n ;
		file write csvfile2 `"`outcome',`outcat',`factr',BIC,`bicw`factr''"' _n ;
		/* file write csvfile `"`outcome',`outcat',`factr',Vuong,`twald`dem'`cost''"' _n ; */
		file write csvfile2 `"`outcome',`outcat',`factr',loglike,`loglike`factr''"' _n ;
    };

	/* ===================== M3 ===================== */
    foreach dem of global dem_vars{;
      foreach cost of global cost_vars{;
		/* di "Processing `outcome'-`dem'-`cost'" ; */
		if "`cost'" == "e_peaveduc" & strpos("`outcat'", "Endog") {;
			ivreghdfe `outcome' (`cost'= `dem' e_migdppcln logpop), absorb(ccode year) resid vce(cluster ccode) ;
		};
		else {;
			reghdfe `outcome' `cost' `dem' e_migdppcln logpop , absorb(ccode year) resid vce(cluster ccode) ;
		};

		capture drop sampletorun ;
		gen sampletorun = e(sample) ;

		mat bb = e(b) ;
        mat eV = e(V) ;
        /*
        capture drop Wsm${m} ;
        capture capture drop Wsm${m}_2;
        predict Wsm${m},res;
        gen Wsm${m}_2=Wsm${m}^2;
        */
        /* scalar rsq${dem}${cost}= e(r2) ;
        local rsq${dem}${cost} : display %6.3f scalar(rsq${m}) ; */
        estat ic ;
        mat aicm = r(S) ;
        /* scalar aicn`dem' =aicm[1,5] ; */
		/* k = e(df_m)+e(df_a)+1 */
        scalar aicn`dem'`cost' = -2*e(ll)+ 2 * (e(df_m)+e(df_a)+1)  + 2*(e(df_m)+e(df_a)+1) *(e(df_m)+e(df_a)+2) /(e(N)-(e(df_m)+e(df_a)+1)-1) ;
		scalar bicn`dem'`cost' = -2*e(ll)+ log(e(N)) * (e(df_m)+e(df_a)+1) ;
        local aic`dem'`cost' : display %10.2f scalar(aicn`dem'`cost') ;
        local bic`dem'`cost' : display %10.2f scalar(bicn`dem'`cost') ;
        local beta2p`dem'`cost' : display %10.2f scalar(bb[1,1]) ;
        local tstat2p`dem'`cost' : display %10.2f scalar(bb[1,1])/sqrt(eV[1,1]) ;
        local loglike`dem'`cost' : display %10.2f scalar(aicm[1, 3]) ;

        file write csvfile2 `"`outcome',`outcat',`dem'+`cost',betap,`beta2p`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost',tstatp,`tstat2p`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost',AIC,`aic`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost',BIC,`bic`dem'`cost''"' _n ;
        /* file write csvfile `"`outcome',`outcat',`dem'`cost',Vuong,`twald`dem'`cost''"' _n ; */
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost',loglike,`loglike`dem'`cost''"' _n ;
		
		if !("`cost'" == "e_peaveduc" & strpos("`outcat'", "Endog")) {;
		  local betaw`dem'`cost' : display %10.2f scalar(bb[1,2]) ;
		  local tstatw`dem'`cost' : display %10.2f scalar(bb[1,2])/sqrt(eV[2,2]) ;
		  file write csvfile2 `"`outcome',`outcat',`dem'+`cost',betaw,`betaw`dem'`cost''"' _n ;
		  file write csvfile2 `"`outcome',`outcat',`dem'+`cost',tstatw,`tstatw`dem'`cost''"' _n ;
		};

		/* ===================== Democracy only ===================== */
		reghdfe `outcome' `dem' e_migdppcln logpop if sampletorun==1, absorb(ccode year) resid vce(cluster ccode) ;
		mat bb_w = e(b) ;
        mat eV_w = e(V) ;
        /*
        capture drop Wsm${m} ;
        capture capture drop Wsm${m}_2;
        predict Wsm${m},res;
        gen Wsm${m}_2=Wsm${m}^2;
        */
        /* scalar rsq${dem}${cost}= e(r2) ;
        local rsq${dem}${cost} : display %6.3f scalar(rsq${m}) ; */
        estat ic ;
        mat aicm = r(S) ;
        /* scalar aicnw`dem' =aicm[1,5] ; */
        scalar aicnw`dem'`cost' =-2*e(ll)+ 2 * (e(df_m)+e(df_a)+1)  + 2*(e(df_m)+e(df_a)+1) *(e(df_m)+e(df_a)+2) /(e(N)-(e(df_m)+e(df_a)+1)-1) ;
		scalar bicnw`dem'`cost' = -2*e(ll)+ log(e(N)) * (e(df_m)+e(df_a)+1) ;
        local aicw`dem'`cost' : display %10.2f scalar(aicnw`dem'`cost') ;
        local bicw`dem'`cost' : display %10.2f scalar(bicnw`dem'`cost') ;
        local betaw`dem'`cost' : display %10.2f scalar(bb_w[1,1]) ;
        local tstatw`dem'`cost' : display %10.2f scalar(bb_w[1,1])/sqrt(eV_w[1,1]) ;
        local loglike`dem'`cost' : display %10.2f scalar(aicm[1, 3]) ;

        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`dem',betaw,`betaw`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`dem',tstatw,`tstatw`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`dem',AIC,`aicw`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`dem',BIC,`bicw`dem'`cost''"' _n ;
        /* file write csvfile `"`outcome',`outcat',`dem',`dem'`cost',Vuong,`twald`dem'`cost''"' _n ; */
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`dem',loglike,`loglike`dem'`cost''"' _n ;

		if "`cost'" == "e_peaveduc" & strpos("`outcat'", "Endog") {;
			ivreghdfe `outcome' (`cost'= e_migdppcln logpop), absorb(ccode year) resid vce(cluster ccode) ;
		};
		else {;
			reghdfe `outcome' `cost' e_migdppcln logpop , absorb(ccode year) resid vce(cluster ccode) ;
		};
		mat bb_p = e(b) ;
        mat eV_p = e(V) ;
        /*
        capture drop Wsm${m} ;
        capture capture drop Wsm${m}_2;
        predict Wsm${m},res;
        gen Wsm${m}_2=Wsm${m}^2;
        */
        /* scalar rsq${dem}${cost}= e(r2) ;
        local rsq${dem}${cost} : display %6.3f scalar(rsq${m}) ; */
        estat ic ;
        mat aicm = r(S) ;
        /* scalar aicp`dem' =aicm[1,5] ; */
        scalar aicnp`dem'`cost' =-2*e(ll)+ 2 * (e(df_m)+e(df_a)+1)  + 2*(e(df_m)+e(df_a)+1) *(e(df_m)+e(df_a)+2) /(e(N)-(e(df_m)+e(df_a)+1)-1) ;
		scalar bicnp`dem'`cost' = -2*e(ll)+ log(e(N)) * (e(df_m)+e(df_a)+1) ;
        local aicp`dem'`cost' : display %10.2f scalar(aicnp`dem'`cost') ;
        local bicp`dem'`cost' : display %10.2f scalar(bicnp`dem'`cost') ;
        local betap`dem'`cost' : display %10.2f scalar(bb_p[1,1]) ;
        local tstatp`dem'`cost' : display %10.2f scalar(bb_p[1,1])/sqrt(eV_p[1,1]) ;
        local loglike`dem'`cost' : display %10.2f scalar(aicm[1, 3]) ;

        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`cost',betap,`betap`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`cost',tstatp,`tstatp`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`cost',AIC,`aicp`dem'`cost''"' _n ;
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`cost',BIC,`bicp`dem'`cost''"' _n ;
        /* file write csvfile `"`outcome',`outcat',`cost',`dem'`cost',Vuong,`twald`dem'`cost''"' _n ; */
        file write csvfile2 `"`outcome',`outcat',`dem'+`cost'/`cost',loglike,`loglike`dem'`cost''"' _n ;
      };
    };
  };
};

file close csvfile2;
