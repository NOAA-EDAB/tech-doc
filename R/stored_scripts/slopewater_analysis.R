## slopewater analysis


#```{octave, eval = F}

function [m1 m2 m3]=my_SLWpercent(T,S);
%
%   analytically determine the proportions of water masses in a given sample,
%   as a combination of three component water masses. T and S can be a vector % of observations.  
%   m1 represents the fraction of the sample that corresponds to Scotian Shelf Water (SSW), m2 the fraction corresponding
%   to Warm Slope Water (WSW) and m3 the fraction corresponding to Labrador
%   Slope Water (LSlW).
%
%   Here we use Cramer's rule to solve the following system of equations:
%   T1*m1 + T2*m2 + T3*m3 = T
%   S1*m1 + S2*m2 + S3*m3 = S
%      m1 +    m2 +    m3 = 1
%
%   p.fratantoni, 6/2011
%

T1=2;S1=32;     % SSW
T2=10;S2=35;    % wSLW
T3=6;S3=34.7;   % cLSW
 
delta=T1*(S2-S3)-S1*(T2-T3)+T2*S3-T3*S2;
 
m1=(T.*(S2-S3)+S.*(T3-T2)+T2*S3-T3*S2)./delta;
m2=(T.*(S3-S1)+S.*(T1-T3)+T3*S1-T1*S3)./delta;
m3=(T.*(S1-S2)+S.*(T2-T1)+T1*S2-T2*S1)./delta;
#```