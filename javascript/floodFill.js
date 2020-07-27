// source: https://codepen.io/Geeyoam/pen/vLGZzG

/**
 * 
 * @param {string} elementId 
 * @param {int} x 
 * @param {int} y 
 * @param {string} color css color, e.g. 'red'
 * @param {float} opacity [0-1]
 */
function floodFill(elementId, x, y, color, opacity) {
  var canvas = document.getElementById(elementId);
  var ctx = canvas.getContext("2d");

  function getColorAtPixel(imageData, x, y) {
    const { width, data } = imageData

    return {
      r: data[4 * (width * y + x) + 0],
      g: data[4 * (width * y + x) + 1],
      b: data[4 * (width * y + x) + 2],
      a: data[4 * (width * y + x) + 3]
    }
  }

  function setColorAtPixel(imageData, color, x, y) {
    const { width, data } = imageData

    data[4 * (width * y + x) + 0] = color.r & 0xff
    data[4 * (width * y + x) + 1] = color.g & 0xff
    data[4 * (width * y + x) + 2] = color.b & 0xff
    data[4 * (width * y + x) + 3] = color.a & 0xff
  }

  function colorMatch(a, b) {
    return a.r === b.r && a.g === b.g && a.b === b.b && a.a === b.a
  }

  function floodFill(imageData, newColor, x, y) {
    const { width, height, data } = imageData
    const stack = []
    const baseColor = getColorAtPixel(imageData, x, y)
    let operator = { x, y }

    // Check if base color and new color are the same
    if (colorMatch(baseColor, newColor)) {
      return
    }

    // Add the clicked location to stack
    stack.push({ x: operator.x, y: operator.y })

    while (stack.length) {
      operator = stack.pop()
      let contiguousDown = true // Vertical is assumed to be true
      let contiguousUp = true // Vertical is assumed to be true
      let contiguousLeft = false
      let contiguousRight = false

      // Move to top most contiguousDown pixel
      while (contiguousUp && operator.y >= 0) {
        operator.y--
        contiguousUp = colorMatch(getColorAtPixel(imageData, operator.x, operator.y), baseColor)
      }

      // Move downward
      while (contiguousDown && operator.y < height) {
        setColorAtPixel(imageData, newColor, operator.x, operator.y)

        // Check left
        if (operator.x - 1 >= 0 && colorMatch(getColorAtPixel(imageData, operator.x - 1, operator.y), baseColor)) {
          if (!contiguousLeft) {
            contiguousLeft = true
            stack.push({ x: operator.x - 1, y: operator.y })
          }
        } else {
          contiguousLeft = false
        }

        // Check right
        if (operator.x + 1 < width && colorMatch(getColorAtPixel(imageData, operator.x + 1, operator.y), baseColor)) {
          if (!contiguousRight) {
            stack.push({ x: operator.x + 1, y: operator.y })
            contiguousRight = true
          }
        } else {
          contiguousRight = false
        }

        operator.y++
        contiguousDown = colorMatch(getColorAtPixel(imageData, operator.x, operator.y), baseColor)
      }
    }
  }

  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
  const col = {...nameToRGB(color), a: opacity }

  floodFill(imageData, col, x, y)
  ctx.putImageData(imageData, 0, 0)
}
