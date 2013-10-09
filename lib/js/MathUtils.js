Math.randgauss = function() {
  var U, V, S, X, Y;
  while (true) {
    U = 2 * Math.random() - 1;
    V = 2 * Math.random() - 1;
    S = U * U + V * V;
    if (0 < S && S < 1) {
      return U * Math.sqrt(-2.0 * Math.log(S) / S);
    }
  }
}
