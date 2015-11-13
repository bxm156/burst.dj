var YoutubeElement = function() {
    var dom = document.createElement( 'div' );
    dom.setAttribute("id", "player");
    dom.style.width = '640px';
    dom.style.height = '390px';

    var object = new THREE.CSS3DObject( dom );
    return object
}