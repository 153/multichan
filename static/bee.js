// an enormous thank you to kig of fhtr.org for his limitless patience, 
// and to sphingonotus for the BEE gif
// HACKED BY CHINESE
var Tension = -4
var right = "/beeR.gif"
var left = "/beeL.gif"

function randomCoord() {
	var x=document.body.scrollLeft||document.documentElement.scrollLeft;
	var y=document.body.scrollTop||document.documentElement.scrollTop;
	var w=window.innerWidth||document.body.offsetWidth;
	var h=window.innerHeight||document.body.offsetHeight;
	return {x:x+Math.round(Math.random()*w),
	y:y+Math.round(Math.random()*h)};
}

function cardinalPoint(u, coords) {
	var u2 = u*u
	var u3 = u2*u
	var s = (1-Tension)/2;
	var CAR0 = -s*u3 + 2*s*u2 - s*u
	var CAR1 = (2-s)*u3 + (s-3)*u2 + 1
	var CAR2 = (s-2)*u3 + (3-2*s)*u2 + s*u
	var CAR3 = s*u3 - s*u2
	return {
		x: Math.floor(coords[0].x * CAR0 + coords[1].x * CAR1 + coords[2].x * CAR2 + coords[3].x * CAR3),
		y: Math.floor(coords[0].y * CAR0 + coords[1].y * CAR1 + coords[2].y * CAR2 + coords[3].y * CAR3)
	};
}

function animate()
{
	(new Image).src=left;
	(new Image).src=right;

	var bee=document.createElement("img");
	bee.style.zIndex=1000;
	bee.style.position="absolute";
	/* for Internet Explorer */
	/*@cc_on @*/
	/*@if (@_win32)
	var iekludge=function() {
		if(document.readyState=="complete") document.body.appendChild(bee);
		else setTimeout(iekludge,100);
	}
	iekludge();
	@else */
	document.body.appendChild(bee);
	/*@end @*/

	var time=0;
	var coords=[randomCoord(),randomCoord(),randomCoord(),randomCoord()];

	setInterval(function() {
		time+=0.03;
		if(time>1) {
			time-=1;
			coords=[coords[1],coords[2],coords[3],randomCoord()];
		}

		var coord=cardinalPoint(time,coords);

		if(coord.x>parseInt(bee.style.left)) {
			if(bee.src!=right) bee.src=right;
		} else {
			if(bee.src!=left) bee.src=left;
		}

		bee.style.left=coord.x+"px";
		bee.style.top=coord.y+"px";
	},40)
}

function tryanimate()
{
	if(document.body) animate();
	else setTimeout(tryanimate,100);
}

tryanimate();
