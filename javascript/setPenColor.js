function setPenColor(canvasId, strokeStyle, x, y) {
    const cnv = document.getElementById(canvasId);
    const ctx = cnv.getContext("2d");
    ctx.beginPath();
    ctx.strokeStyle = strokeStyle;
    ctx.moveTo(x, y);
}
