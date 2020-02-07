-- !preview conn=DBI::dbConnect(RSQLite::SQLite())

/*```{sql, eval = F, echo = T}
/* training trips, 900 trips, incidental takes, most duplicate records 
(unless different idmethod or idcomment) are not included */
/* this is a general script to pull the data on any species from the SVP*/
/* specimens submitted as photos and samples included separately */
/* nefop_ims.species_verification query that approximates is: select * 
from nefop_ims.species_verification where SUBJECT_CODE <> '01' and YEAR > 
'2009' and species = '6617' order by species, year, tripid, haulnum, 
idmethod but this could includes training trips, duplicates, 900 trips*/


SELECT ss.year YEAR, MONTH, ss.obid as OBSID, ss.tripid TRIPID, NEGEAR, DATELAND, 
SS.HAUL HAUL, CODE, SPECIES, correct, INCCODE, INCORRECTSPP, idmethod, GIS_LATSBEG, 
GIS_LONSBEG, GIS_LATSEND, GIS_LONSEND, GIS_LATHBEG, GIS_LONHBEG, GIS_LATHEND, 
GIS_LONHEND, rr.QTR QTR, rr.link1 link1, rr.link3 LINK3, idcomments

from 

(SELECT substr(c.tripid, 1,3) obid, c.tripid, c.year, HAUL, 
TO_CHAR(t.dateland, 'DD-MON-YY') as DATELAND, CODE, SPECIES, correct, 
INCORRECTSPP as INCCODE, comname as INCORRECTSPP, idmethod, idcomments

FROM 

(select id_num, a.tripid, a.year, lpad(CAST(haulnum as varchar2(4 byte)),4,'0') haul, 
inc, dateverify, species as CODE, comname as SPECIES, correct, incorrectspp,
  idmethod, idcomments, obs_contacted, filelocation
from nefop_ims.species_verification a, obdbs.obspec b
where a.species=b.nespp4) c 
left join obdbs.obspec d 
on c.incorrectspp=d.nespp4
join OBSCON.OBSCON_TRIPS_FSB t on c.year||c.tripid=t.year||substr(t.LINK1,10,6)
where c.YEAR like '%%' and c.TRIPID like '%%' and c.inc is null and DATELAND between 
to_date('01-JAN-10', 'DD-MON-RR') and to_date('31-DEC-20','DD-MON-RR')

UNION

SELECT substr(g.tripid,1,3) obid, g.tripid, g.year, HAUL, TO_CHAR(s.dateland, 'DD-MON-YY') 
as DATELAND, CODE, SPECIES, correct, INCORRECTSPP as INCCODE, comname as INCORRECTSPP,
  idmethod, idcomments
FROM ((select id_num, e.tripid, e.year, lpad(CAST(haulnum as varchar2(4 byte)),4,'0') haul,
inc, dateverify, species as CODE, comname as SPECIES, correct, incorrectspp,
  idmethod, idcomments, obs_contacted, filelocation
from nefop_ims.species_verification e, obdbs.obspec f
where e.species=f.nespp4) g 
left join obdbs.obspec h 
on g.incorrectspp=h.nespp4
join obdbs.asmtrp_entry s on g.year||g.tripid=s.yearland||s.tripid) 
where g.YEAR like '%%' and g.TRIPID like '%%' and g.inc is null and DATELAND between 
to_date('01-JAN-10', 'DD-MON-RR') and to_date('31-DEC-20','DD-MON-RR')

UNION

SELECT substr(r.tripid, 1,3) obid, r.tripid, r.year, HAUL, 
TO_CHAR(s.dateland, 'DD-MON-YY') as DATELAND, CODE, SPECIES, correct, 
INCORRECTSPP as INCCODE, comname as INCORRECTSPP,
  idmethod, idcomments
FROM ((select id_num, a.tripid, a.year, lpad(CAST(haulnum as varchar2(4 byte)),4,'0') 
haul, inc, dateverify, species as CODE, comname as SPECIES, correct, incorrectspp,
  idmethod, idcomments, obs_contacted, filelocation
from nefop_ims.species_verification a, obdbs.obspec b
where a.species=b.nespp4) r 
left join obdbs.obspec d 
on r.incorrectspp=d.nespp4
join OBPRELIM.TRP_BASE s on r.year||r.tripid=s.yearland||S.TRIPID)
where r.YEAR like '%%' and r.TRIPID like '%%' and r.inc is null and DATELAND
between to_date('01-JAN-10', 'DD-MON-RR') and to_date('31-DEC-20','DD-MON-RR')) ss

left join

(/* OBDBS OBHAU */

select
   substr(link3,1,15)  LINK1 ,
   LINK3,   
   substr(link3,1,3)  PROGRAM ,
   substr(link3,4,4)   YEAR ,
   substr(link3,8,2)   MONTH ,
   substr(link3,10,6)  TRIPID ,
   substr(link3,16,4)  HAULNUM ,
   decode(substr(link3,8,2),'01',1,'02',1,'03',1,'04',2,
           '05',2,'06',2,'07',3,'08',3,'09',3,'10',4,'11',4,'12',4,null) QTR,
 NEGEAR,
 OBSRFLAG,
 CATEXIST,
case when yearhbeg is not null and monthhbeg is not null and dayhbeg is not null 
then
   to_date(ltrim(rtrim(YEARHBEG))||ltrim(rtrim(MONTHHBEG))||ltrim(rtrim(DAYHBEG))||
   ltrim(rtrim(TIMEHBEG)),
   'YYYYMMDDHH24MI')
else null
end datehbeg,
case when yearhend is not null and monthend is not null and dayhend is not null then
   to_date(ltrim(rtrim(YEARHEND))||ltrim(rtrim(MONTHEND))||ltrim(rtrim(DAYHEND))||
   ltrim(rtrim(TIMEHEND)),'YYYYMMDDHH24MI')
else null
end datehend,
 LATHBEG,
 LONHBEG,
 LATHEND,
 LONHEND,
 cast( substr(latsbeg,1,2) + substr(latsbeg,3,2) / 60 + 
 substr(latsbeg,5,2) / 3600 as number(8,6)) GIS_LATSBEG ,
 -1 * cast(substr(lonsbeg,1,2) + substr(lonsbeg,3,2) / 60 +
 substr(lonsbeg,5,2) / 3600 as number(8,6)) GIS_LONSBEG ,
  cast(substr(latsend,1,2) + substr(latsend,3,2) / 60 + 
  substr(latsend,5,2) / 3600 as number(8,6)) GIS_LATSEND,
  -1 * cast(substr(lonsend,1,2) + substr(lonsend,3,2) / 60 + 
  substr(lonsend,5,2) / 3600 as number(8,6)) GIS_LONSEND,
 cast(substr(lathbeg,1,2) + substr(lathbeg,3,2) / 60 + 
 substr(lathbeg,5,2) / 3600 as number(8,6)) GIS_LATHBEG,
 -1 * cast(substr(lonhbeg,1,2) + substr(lonhbeg,3,2) / 60 + 
 ubstr(lonhbeg,5,2) / 3600 as number(8,6)) GIS_LONHBEG,
 cast(substr(lathend,1,2) + substr(lathend,3,2) / 60 + 
 substr(lathend,5,2) / 3600 as number(8,6)) GIS_LATHEND,
 -1 * cast(substr(lonhend,1,2) + substr(lonhend,3,2) / 60 + 
 substr(lonhend,5,2) / 3600 as number(8,6)) GIS_LONHEND,
 AREA,
 HAUCOMMENTS
   from obdbs.obhau_base

    
UNION
    select
   substr(link3,1,15)  LINK1 ,
   LINK3,
   substr(link3,1,3)  PROGRAM ,
   substr(link3,4,4)   YEAR ,
   substr(link3,8,2)   MONTH ,
   substr(link3,10,6)  TRIPID ,
   substr(link3,16,4)  HAULNUM ,
   decode(substr(link3,8,2),'01',1,'02',1,'03',1,'04',2,
           '05',2,'06',2,'07',3,'08',3,'09',3,'10',4,'11',4,'12',4,null) QTR,

 NEGEAR,
 OBSRFLAG,
 CATEXIST,
case when yearhbeg is not null and monthhbeg is not null and dayhbeg is 
not null then
   to_date(ltrim(rtrim(YEARHBEG))||ltrim(rtrim(MONTHHBEG))||ltrim(rtrim(DAYHBEG))|
   |ltrim(rtrim(TIMEHBEG)),'YYYYMMDDHH24MI')
else null
end datehbeg,
case when yearhend is not null and monthend is not null and dayhend is not null then
   to_date(ltrim(rtrim(YEARHEND))||ltrim(rtrim(MONTHEND))||ltrim(rtrim(DAYHEND))|
   |ltrim(rtrim(TIMEHEND)),'YYYYMMDDHH24MI')
else null
end datehend,
 LATHBEG,
 LONHBEG, 
 LATHEND,
 LONHEND,
 cast( substr(latsbeg,1,2) + substr(latsbeg,3,2) / 60 + 
 substr(latsbeg,5,2) / 3600 as number(8,6)) GIS_LATSBEG ,
 -1 * cast(substr(lonsbeg,1,2) + substr(lonsbeg,3,2) / 60 + 
 substr(lonsbeg,5,2) / 3600 as number(8,6)) GIS_LONSBEG ,
 cast(substr(latsend,1,2) + substr(latsend,3,2) / 60 + 
 substr(latsend,5,2) / 3600 as number(8,6)) GIS_LATSEND,
 -1 * cast(substr(lonsend,1,2) + substr(lonsend,3,2) / 60 + 
 substr(lonsend,5,2) / 3600 as number(8,6)) GIS_LONSEND,
 cast(substr(lathbeg,1,2) + substr(lathbeg,3,2) / 60 + 
 substr(lathbeg,5,2) / 3600 as number(8,6)) GIS_LATHBEG,
 -1 * cast(substr(lonhbeg,1,2) + substr(lonhbeg,3,2) / 60 + 
 substr(lonhbeg,5,2) / 3600 as number(8,6)) GIS_LONHBEG,
 cast(substr(lathend,1,2) + substr(lathend,3,2) / 60 + 
 substr(lathend,5,2) / 3600 as number(8,6)) GIS_LATHEND,
 -1 * cast(substr(lonhend,1,2) + substr(lonhend,3,2) / 60 + 
 substr(lonhend,5,2) / 3600 as number(8,6)) GIS_LONHEND,
 AREA,
 HAUCOMMENTS
   from obv10.obhau_base


UNION

/*  ASM HAU  */

select
   substr(link3,1,15)  LINK1 ,
   LINK3,
   substr(link3,1,3)  PROGRAM ,
   substr(link3,4,4)   YEAR ,
   substr(link3,8,2)   MONTH ,
   substr(link3,10,6)  TRIPID ,
   substr(link3,16,4)  HAULNUM ,

   decode(substr(link3,8,2),'01',1,'02',1,'03',1,'04',2,
           '05',2,'06',2,'07',3,'08',3,'09',3,'10',4,'11',4,'12',4,null) QTR,
 NEGEAR,
 OBSRFLAG,
 cast(null as varchar2(1)) CATEXIST,
   to_date(ltrim(rtrim(YEARHBEG))||ltrim(rtrim(MONTHHBEG))|
   |ltrim(rtrim(DAYHBEG))||ltrim(rtrim(TIMEHBEG)),'YYYYMMDDHH24MI')datehbeg, 
   to_date(ltrim(rtrim(YEARHEND))||ltrim(rtrim(MONTHEND))|
   |ltrim(rtrim(DAYHEND))||ltrim(rtrim(TIMEHEND)),'YYYYMMDDHH24MI')datehend, 
 LATHBEG,
 LONHBEG,
 LATHEND,
 LONHEND,
 cast(null as number(8,6)) GIS_LATSBEG ,
 cast(null as number) GIS_LONSBEG ,
 cast(null as number(8,6)) GIS_LATSEND,
 cast(null as number) GIS_LONSEND,
 cast(substr(lathbeg,1,2) + substr(lathbeg,3,2) / 60 + 
 substr(lathbeg,5,2) / 3600 as number(8,6)) GIS_LATHBEG,
 -1 * cast(substr(lonhbeg,1,2) + substr(lonhbeg,3,2) / 60 + 
 substr(lonhbeg,5,2) / 3600 as number(8,6)) GIS_LONHBEG,
 cast(substr(lathend,1,2) + substr(lathend,3,2) / 60 + 
 substr(lathend,5,2) / 3600 as number(8,6)) GIS_LATHEND,
 -1 * cast(substr(lonhend,1,2) + substr(lonhend,3,2) / 60 + 
 substr(lonhend,5,2) / 3600 as number(8,6)) GIS_LONHEND,
 AREA,
 HAUCOMMENTS
 
   from asmhau_prelim p
 left outer join obtriptrack t 
      on substr(p.link3,1,15) = t.link1 
  where (substr(link3,4,6) between '201005' and '201012' and 
  substr(link3,1,3) between '230' and '234')
     or (substr(link3,4,6) > '201012' and substr(link3,1,3) <> '900')
    and substr(link3,1,15) not in (select link1 from obv10.obtrp_base) ) rr
    
on ss.YEAR||ss.TRIPID||ss.HAUL = rr.YEAR||rr.TRIPID||ltrim(rr.HAULNUM)

where ss.OBID like '%%' and ss.TRIPID like '%%' and (CODE like '%6617%') 
and HAUL like '%%' and SPECIES like '%%' and IDCOMMENTS like '%%' 

ORDER BY SPECIES, YEAR, TRIPID, HAUL
;


