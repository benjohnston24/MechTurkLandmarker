function check(obj) {
    acc = [];
    if ((obj.P1 && obj.P1[0]) > (obj.P2 && obj.P2[0])) acc.push("P2 is to the left of P1, are they switched around?");
    return acc;
}
