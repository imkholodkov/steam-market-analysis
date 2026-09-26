// Настройка MathJax для pymdownx.arithmatex (generic: true), по документации Material for MkDocs
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

document$.subscribe(() => {
  MathJax.startup.output.clearCache?.(); // есть только у CHTML-вывода
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
