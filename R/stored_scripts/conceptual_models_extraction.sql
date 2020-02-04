/* conceptual models extraction*/



/*```{sql FEAST, eval = F, echo = T}*/
Select svspp,year,cruise6,stratum,station,catsex,pdid,pdgutw,pdlen,pdwgt,
perpyw,pyamtw,COLLCAT,numlen,pyamtv  from fhdbs.allfh_feast where pynam 
<> 'BLOWN' and pynam <> 'PRESERVED' and pynam <> ' ' and svspp='073' and 
YEAR BETWEEN '1973' AND '2016' and GEOAREA='GB' order by svspp,year,
cruise6,stratum,station,pdid,COLLCAT
Select distinct svspp,year,cruise6,stratum,station from fhdbs.allfh_feast 
where pynam <> 'BLOWN' and pynam <> 'PRESERVED' and pynam <> ' ' and 
svspp='073' and YEAR BETWEEN '1973' AND '2016' and GEOAREA='GB' order by 
svspp,year,cruise6,stratum,station
Select distinct svspp,year,cruise6,stratum,station,catsex,catnum from 
fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 'PRESERVED' and 
pynam <> ' ' and svspp='073' and YEAR BETWEEN '1973' AND '2016' and 
GEOAREA='GB' order by svspp,year,cruise6,stratum,station
Select distinct COLLCAT from fhdbs.allfh_feast where pynam <> 'BLOWN' and 
pynam <> 'PRESERVED' and pynam <> ' ' and svspp='073' and YEAR BETWEEN '1973' 
AND '2016' and GEOAREA='GB' order by COLLCAT
Select distinct svspp,year,cruise6,stratum,station,catsex,pdid,pdlen,pdgutw,
pdwgt  from fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 'PRESERVED'
and pynam <> ' ' and svspp='073' and YEAR BETWEEN '1973' AND '2016' and
GEOAREA='GB' order by svspp,year,cruise6,stratum,station,catsex,pdid
Select svspp,year,cruise6,stratum,station,catsex,pdid,pdlen,COLLCAT,sum(perpyw),
sum(pyamtw),sum(pyamtv)  from fhdbs.allfh_feast where pynam <> 'BLOWN' and 
pynam <> 'PRESERVED' and pynam <> ' ' and svspp='073' and YEAR BETWEEN '1973' 
AND '2016' and GEOAREA='GB' group by svspp,year,cruise6,stratum,station,catsex,
pdid,pdlen,COLLCAT order by svspp,year,cruise6,stratum,station,catsex,pdid,
pdlen,COLLCAT
Select svspp,year,cruise6,stratum,station,COLLCAT,sum(pyamtv) sumpvol from 
fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 'PRESERVED' and pynam 
<> ' ' and svspp='073' and YEAR BETWEEN '1973' AND '2016' and GEOAREA='GB'
group by svspp,year,cruise6,stratum,station,
COLLCAT order by svspp,year,
cruise6,stratum,station,COLLCAT
Select svspp,year,cruise6,stratum,station, count(distinct pdid) nstom  
from fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 'PRESERVED' 
and pynam <> ' ' and svspp='073' and YEAR BETWEEN '1973' AND '2016' 
and GEOAREA='GB' group by svspp,year,cruise6,stratum,station,catsex order by 
svspp,year,cruise6,stratum,station
Select svspp,year,cruise6,stratum,station,pdlen,numlen,count(distinct pdid) 
nstom  from fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 
'PRESERVED' and pynam <> ' ' and numlen is not null and svspp='073' and 
YEAR BETWEEN '1973' AND '2016' and GEOAREA='GB' group by svspp,year,
cruise6,stratum,station,pdlen,numlen,catsex order by svspp,year,cruise6,
stratum,station,pdlen
Select svspp,year,cruise6,stratum,station,pdlen,
COLLCAT,sum(pyamtv) sumpvol 
from fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 'PRESERVED' and 
pynam <> ' ' and svspp='073' and YEAR BETWEEN '1973' AND '2016' and 
GEOAREA='GB' group by svspp,year,cruise6,stratum,station,pdlen,
COLLCAT order by svspp,year,cruise6,stratum,station,pdlen,CFOLLCAT
Select distinct svspp,year,cruise6,stratum,station,pdid,pdlen from 
fhdbs.allfh_feast where pynam <> 'BLOWN' and pynam <> 'PRESERVED' and pynam <>
' ' and numlen is null and svspp='073' and YEAR BETWEEN '1973' AND '2016' and
GEOAREA='GB'
Select distinct year,cruise6,stratum,station,beglat,beglon  from fhdbs.allfh_feast
where pynam <> 'BLOWN' and pynam <> 'PRESERVED' and pynam <> ' ' and svspp='073'
and YEAR BETWEEN '1973' AND '2016' and GEOAREA='GB' order by year,cruise6,stratum,station

