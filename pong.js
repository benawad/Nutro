//Create the renderer
var renderer = PIXI.autoDetectRenderer(
  256, 256,
  {antialias: false, transparent: false, resolution: 1}
);

//Add the canvas to the HTML document
document.body.appendChild(renderer.view);

//Create a container object called the `stage`
var stage = new PIXI.Container();

//Tell the `renderer` to `render` the `stage`
renderer.render(stage);

renderer.view.style.border = "1px dashed black";
renderer.backgroundColor = 0x061639;
renderer.autoResize = true;
renderer.resize(512, 512);



function setup() {

  var graphics = new PIXI.Graphics();

  graphics.beginFill(0xFFFFFF);

  // set the line style to have a width of 5 and set the color to red
  graphics.lineStyle(5, 0xFFFFFF);

  // draw a rectangle
  graphics.drawRect(0, 0, 300, 200);
  renderer.render(stage);
}
