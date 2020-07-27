function makeTurtle(canvasId, lineWidth, strokeStyle, fillStyle) {
    const cnv = document.getElementById(canvasId);
    const ctx = cnv.getContext("2d");
    ctx.lineWidth = {lineWidth};
    ctx.strokeStyle = strokeStyle;
    ctx.fillStyle = fillStyle;
}