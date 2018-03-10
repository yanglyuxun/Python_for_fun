select min(p1.x-p2.x) shortest
from point p1, point p2
where p1.x > p2.x;
