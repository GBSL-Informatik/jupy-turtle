function nameToRGB(name) {
    // Get RGB from named color in temporary div
    let fakeDiv = document.createElement("div");
    fakeDiv.style.color = name;
    document.body.appendChild(fakeDiv);

    let cs = window.getComputedStyle(fakeDiv);
    let pv = cs.getPropertyValue("color");

    document.body.removeChild(fakeDiv);
    rgb = pv.substr(4).split(")")[0].split(",").map((n) => Number.parseInt(n))

    return { r: rgb[0], g: rgb[1], b: rgb[2] };
}