function setPenWidth(canvasId, lineWidth) {
    const cnv = document.getElementById(canvasId);
    const ctx = cnv.getContext("2d");
    ctx.beginPath();
    ctx.lineWidth = lineWidth;
}
