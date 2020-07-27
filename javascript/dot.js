function dot(canvasId, x, y, diameter) {
    const cnv = document.getElementById(canvasId);
    const ctx = cnv.getContext("2d");
    ctx.beginPath();
    ctx.arc(x, y, diameter / 2, 0, 2 * Math.PI, false);
    ctx.fill();
    ctx.stroke();
    ctx.moveTo(x, y);
    ctx.end
}
