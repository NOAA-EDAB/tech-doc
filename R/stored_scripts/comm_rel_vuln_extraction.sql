/* Commercial reliance vulnerability indicator extraction

/*```{sql, eval = F, echo = T}*/
create table cfders2011 as
select *
from connection to oracle
(select port, state, year, dealnum, permit, nespp3, spplndlb, sppvalue from cfders2011 where permit > 0 order by permit);
create table cfvess11 as
select *
from connection to oracle
(select permit, homeport, homest from CFDBS.cfvess11 where permit > 0 order by permit);
create table port_name as
select *
from connection to oracle
(select port, portnm from port order by port);
create table st_name as
select *
from connection to oracle
(select state, stateabb from statenm order by state);


Truncated SAS code:

/*CREATE VARIABLES FOR TOTAL LANDINGS WEIGTH AND VALUE (SUM) BY PORT OF LANDING AND BY HOMEPORT*/
data landings_ports1; set landings_ports;
run;
proc sort;
by port state;
run;
proc means noprint data = landings_ports1; by port state; 
var spplndlb sppvalue;
id port state;
output out = landport_totspp sum = L_Totlb L_Totval;
run;
proc sort;
by port;
run;
data landings_ports2; set landings_ports;
run;
proc sort;
by homeport homest;
run;
proc means noprint data = landings_ports2; by homeport homest; 
var spplndlb sppvalue;
id homeport homest;
output out = homeport_totspp sum = H_Totlb H_Totval;
run;
proc sort;
by homeport;
run;

/*CREATE SPECIES VARIABLES*/
data landings_ports_NE_spp; set landings_ports;
monklb = 0; monkval = 0; /*monkfish*/
bluelb = 0; blueval = 0; /*bluefish*/
.omitted.
otherlb = 0; otherval = 0; /*other - everything else*/
run;
data landings_ports_NE_spp2; set landings_ports_NE_spp;
if nespp3 = 012 then do; monklb = spplndlb; monkval = sppvalue; end;
...ommitted.
if nespp3 = 406 then do; spotlb = spplndlb; spotval = sppvalue; end;
if nespp3 not in (012, 023, 033, 051, 081, 105, 112, 115, 116, 120, 121, 122, 123, 124, 125, 132, 147, 152, 153, 155, 159, 168, 194, 197, 212, 
221, 240, 250, 269, 305, 329, 330, 335, 344, 345, 351, 352, 365, 366, 367, 368, 369, 370, 372, 373, 384, 415, 418, 432, 438, 443, 444, 445, 
446, 447, 464, 466, 467, 468, 469, 470, 471, 472, 507, 508, 509, 512, 517, 700, 710, 711, 724, 727, 748, 754, 769, 774, 775, 781, 786, 789, 
798, 799, 800, 801, 802, 805, 806, 899, 001, 090, 069, 107, 150, 173, 196, 334, 347, 349, 364, 371, 420, 422, 481, 484, 714, 776, 777, 823, 763, 736) 
then do; otherlb = spplndlb; otherval = sppvalue; end;
run; 

/*SUM SPECIES LANDINGS BY PORT OF LANDING*/
proc sort; by port; proc means noprint data = landings_ports_NE_spp2; by port state; 
. omitted ...
id port state;
output out = spp_porlnd_NE sum = ;
run;
proc sort;
by port;
run;

/*SUM SPECIES LANDINGS BY HOMEPORT*/
data spp_home; set landings_ports_NE_spp2;
run;
proc sort; by homeport homest; proc means noprint data = spp_home; by homeport homest; 
. species are counted..
id homeport homest;
output out = spp_homep_NE sum = ;
run
proc sort;
by homeport; run;

/*MERGE TOTAL PERMITS AND TOTAL DEALERS BY PORT OF LANDING*/
data land_port_totperm2; set land_port_totperm;
run;
proc sort;
by port; run;
data lnd_port_permit; merge spp_porlnd_NE (IN=X) land_port_totperm2 (IN=Y);
by port; if X=1; run;data land_port_totdeal2; set land_port_totdeal;
run;
proc sort;
by port;
run;
data lnd_port_permit_deal; merge lnd_port_permit (IN=x) land_port_totdeal2 (IN=Y);
by port; if X=1; run;

/*MERGE WITH PORT NAME AND STATE ABBREVIATION*/
data lnd_port_permit_deal_nm; merge lnd_port_permit_deal (IN=X) port_name (IN=Y);
by port; if X=1; run;
data lnd_port_permit_deal_nm_st; merge lnd_port_permit_deal_nm (IN=x) st_name (IN=Y); proc sort;
by port; if X=1; run;

/*MERGE TOTAL PERMITS AND TOTAL DEALERS BY HOMEPORT*/
data home_port_totperm2; set home_port_totperm;
run;
proc sort;
by homeport;
run;
data home_port_permit; merge spp_homep_NE (IN=X) home_port_totperm2 (IN=Y);
by homeport; if X=1; run; data home_port_totdeal2; set home_port_totdeal;
run;
proc sort;
by homeport;
run;
data home_port_permit_deal; merge home_port_permit (IN=x) home_port_totdeal2 (IN=Y);
by homeport; if X=1; run; proc sort;
by homeport;
run;

/*MERGE TOTAL LANDINGS BY PORT OF LANDING*/
data lnd_port_per_deal_nm_st_tspp; merge lnd_port_permit_deal_nm_st (IN=X) landport_totspp (IN=Y);
by port; if X=1; run;

/*MERGE TOTAL LANDINGS BY HOMEPORT*/
data home_port_per_deal_tspp; merge home_port_permit_deal (IN=X) homeport_totspp (IN=Y);
by homeport; if X=1; run;
data netana.port_landing11; set lnd_port_per_deal_nm_st_tspp;
if state in (22, 32, 24, 42, 7, 35, 33, 8, 23, 49, 36);
run;
proc sort;
by port state;
run;
data netana.homeport11; set home_port_per_deal_tspp;
if homest in ('ME', 'NH', 'MA', 'RI', 'CT', 'NY', 'NJ', 'DE', 'MD', 'VA', 'NC');
run;
proc sort;
by homeport homest;
run;


/*```