function moveTurtleTo(canvasId, x, y) {
    let cnv = document.getElementById(canvasId);
    let ctx = cnv.getContext("2d");
    ctx.moveTo(x, y)
}
