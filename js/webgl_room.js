
var CORE = CORE || {};

CORE.init = function (){
    this.sceneCSS = new THREE.Scene();
    this.sceneGL = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera( 75, $('#viewer').width() / $('#viewer').height(), 0.1, 1000 );

    this.rendererCSS = new THREE.CSS3DRenderer();
    this.rendererCSS.domElement.style.position = 'absolute';
    this.rendererCSS.domElement.style.top = 0;
    this.rendererCSS.domElement.style.margin = 0;
    this.rendererCSS.domElement.style.padding = 0;
    this.rendererCSS.setClearColor( 0x343434, 1);
    this.rendererCSS.setSize( $('#viewer').width(), $('#viewer').height() );
    document.getElementById( 'viewer' ).appendChild( this.rendererCSS.domElement );
    

    this.rendererGL = new THREE.WebGLRenderer({alpha:true, antialias: true});
    this.rendererGL.setClearColor(0x000000, 0);

    this.rendererGL.setSize( $('#viewer').width(), $('#viewer').height() );

    this.rendererGL.domElement.style.position = 'absolute';
    this.rendererGL.domElement.style.zIndex = 1;
    this.rendererGL.domElement.style.top = 0;
    this.rendererGL.domElement.style.left = 0;
    this.rendererCSS.domElement.appendChild(this.rendererGL.domElement);

    this.camera.position.x = 400;
    this.camera.position.y = -50;
    this.camera.position.z = 400;

    this.initControls();
    this.initLights();
    this.initGeometry();
    this.initBoth();
    this.animate();
};

CORE.initGeometry = function()
{
    var geometry = new THREE.BoxGeometry( 50, 50, 50 );
    var material = new THREE.MeshPhongMaterial({
        color: 0xffffff,
        emissive: 0x0000ff,
        side: THREE.DoubleSide,
        shading: THREE.FlatShading
    })
    var cubeCenter = new THREE.Mesh( geometry, material );
    cubeCenter.position.x = 300;
    cubeCenter.position.y = -125;
    cubeCenter.position.z = 210;
    cubeCenter.rotation.y = Math.PI / 4
    CORE.sceneGL.add(cubeCenter);

    var cubeX = new THREE.Mesh( geometry, material );
    cubeX.position.x = 600;
    cubeX.position.y = -125;
    cubeX.position.z = 180;
    cubeX.rotation.y = Math.PI / 3
    CORE.sceneGL.add(cubeX);
}


CORE.initLights = function(){
    var light = new THREE.SpotLight();
    light.position.set( 10, 10, 10 );
    light.intensity = 0.5;
    light.castShadow = true;
    CORE.sceneGL.add(light);

    var ambientlight = new THREE.AmbientLight(0x404040);
    CORE.sceneGL.add(ambientlight);
};


CORE.animate = function()
{
    requestAnimationFrame(CORE.animate);
    CORE.controls.update();
    CORE.rendererCSS.render(CORE.sceneCSS, CORE.camera);
    CORE.rendererGL.render(CORE.sceneGL, CORE.camera);
};

CORE.initControls = function(){
    this.controls = new THREE.OrbitControls(
        this.camera,
        this.rendererCSS.domElement
    );
};

CORE.initBoth = function(){
    // create the plane mesh
    var material   = new THREE.MeshBasicMaterial();
    material.color.set('black')
    material.opacity   = 0;
    material.blending  = THREE.NoBlending;
    var geometry = new THREE.PlaneGeometry();
    var planeMesh= new THREE.Mesh( geometry, material );
    // add it to the WebGL scene
    CORE.sceneGL.add(planeMesh);

    // create the dom Element
     var dom = document.createElement( 'div' );
    dom.setAttribute("id", "player");
    dom.style.width = '640px';
    dom.style.height = '390px';
    // create the object3d for this element
    var cssObject = new THREE.CSS3DObject( dom );
    // we reference the same position and rotation 
    cssObject.position = planeMesh.position;
    cssObject.rotation = planeMesh.rotation;
    // add it to the css scene
    CORE.sceneCSS.add(cssObject);
}

console.log('Initializing WebGL')
CORE.init();

