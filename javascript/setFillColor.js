function setFillColor(canvasId, fillStyle) {
    const cnv = document.getElementById(canvasId);
    const ctx = cnv.getContext("2d");
    ctx.fillStyle = fillStyle;
}
