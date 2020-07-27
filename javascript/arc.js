function arc(canvasId, centerX, centerY, radius, startAngle, endAngle, antiClockwise) {
    const cnv = document.getElementById(canvasId);
    const ctx = cnv.getContext("2d");
    ctx.arc(centerX, centerY, radius, startAngle, endAngle, antiClockwise);
    ctx.stroke();
}
