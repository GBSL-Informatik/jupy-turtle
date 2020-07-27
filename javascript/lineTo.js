function lineTo(canvasId, x, y) {
    const c = document.getElementById(canvasId);
    const ctx = c.getContext("2d");
    ctx.lineTo(x, y);
    ctx.stroke();
}
