
(function(){
	var dim = {
		l: 80,
		h: 80
	};
	var fixed_pos = {
		x: 400,
		y: 540
	}
    var states = [];
    for(var i = -6; i < 6; i++){
    	for(var j = -6; j < 10; j++){
    		states.push([
    			fixed_pos.x + i * dim.l, 
    			fixed_pos.y + j * dim.h,
    			fixed_pos.x + (i + 1) * dim.l,
    			fixed_pos.y + (j + 1) * dim.h
    		]);
    	}
    }

    var rewards = {
        target: 1000,
        out: -1000,
        stable: -1
    };
    var actions = {
        up: { x: 0.2, y: 0 },
        left: { x: -0.2, y: 0 },
        right: { x: 0, y: -0.2 }
    };

    var Q = [];

    for(var i = 0; i < states.length; i++){
    	Q.push([]);
    	for(var j = 0; j < Object.keys(actions).length; j++){
    		Q[i].push(Math.random());
    	}
    }

    var lr = 0.3
    var df = 0.6

    

    var Engine = Matter.Engine,
        Render = Matter.Render,
        World  = Matter.World,
        Bodies = Matter.Bodies;

    var engine = Engine.create();

    var render = Render.create({
        element: document.body,
        engine: engine
    });

    boxA = Bodies.rectangle(350, 200, dim.l, dim.h);
    var boxB = Bodies.rectangle(fixed_pos.x, fixed_pos.y, dim.l, dim.h, {isStatic: true});
    var ground = Bodies.rectangle(400, 610, 600, 60, { isStatic: true });

    var shapes_array = [boxA, boxB, ground];
    var current_box = boxA;

    engine.world.gravity.y = 0;
    World.add(engine.world, shapes_array);

    document.addEventListener('keydown', function(event) {
        if(event.keyCode == 39) {
            force = { x: 0.2, y: 0 };
            Matter.Body.applyForce(current_box, current_box.position, force);
        }
        if(event.keyCode == 37) {
            force = { x: -0.2, y: 0 };
            Matter.Body.applyForce(current_box, current_box.position, force);
        }
        if(event.keyCode == 38) {
            force = { x: 0, y: -0.2 };
            Matter.Body.applyForce(current_box, current_box.position, force);
        }
        if(event.keyCode == 40) {
            force = { x: 0, y: 0.2 };
            Matter.Body.applyForce(current_box, current_box.position, force);
        }
        if(event.keyCode == 32) {
            var newbox = Bodies.rectangle(450, 50, 80,80);
            shapes_array.push(newbox)
            World.add(engine.world, newbox);
            current_box = newbox;
        }
    });

    Engine.run(engine);
    Render.run(render);


    var cg = {
    	x: boxA.position.x + dim.l/2, 
    	y: boxA.position.y + dim.h/2
    };
    
    var current_state;
    for(var i = 0; i < states.length; i++){
    	if(cg.x > states[i][0] && cg.x < states[i][2] && cg.y > states[i][1] && cg.y < states[i][3]){
    		current_state = states[i]
    	}
    }
    console.log(current_state)
    // while(){

    // }
})()
