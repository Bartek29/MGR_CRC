point AL 30 10
point BL 30 50
point CL 30 80

#line AL BL
#line BL CL
line AL CL

point AR 80 10
point BRL 80 50
point BRH 60 50
point CR 60 80

bezier AL AR BRL BL
bezier BL BRH CR CL