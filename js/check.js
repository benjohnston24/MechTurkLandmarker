function check(obj) {
    acc = [];
    if ((obj.P1 && obj.P1[0]) < (obj.P2 && obj.P2[0])) acc.push("P2 is to the right of P1, are they switched around?");
    if ((obj.P1 && obj.P1[1]) > (obj.P2 && obj.P2[1])) acc.push("P2 is above P1, are they switched around?");
    if ((obj.P2 && obj.P2[1]) > (obj.P3 && obj.P3[1])) acc.push("P3 is above P2, are they switched around?");
    if ((obj.P3 && obj.P3[1]) > (obj.P4 && obj.P4[1])) acc.push("P4 is above P3, are they switched around?");
    if ((obj.P3 && obj.P3[0]) < (obj.P5 && obj.P5[0])) acc.push("P5 is to the right of P3, are they switched around?");
    if ((obj.P4 && obj.P4[1]) > (obj.P5 && obj.P5[1])) acc.push("P5 is above P4, are they switched around?");
    if ((obj.P5 && obj.P5[0]) < (obj.P6 && obj.P6[0])) acc.push("P6 is to the right of P5, are they switched around?");
    if ((obj.P5 && obj.P5[1]) > (obj.P6 && obj.P6[1])) acc.push("P5 is above P4, are they switched around?");
    return acc;
}
