
(function(){
    state = {
        
    };
    reward = {
        target: 1000,
        out: -1000,
        stable: 0
    }
    actions = {
        up: { x: 0.2, y: 0 },
        left: { x: -0.2, y: 0 },
        right: { x: 0, y: -0.2 }
    }

    var Engine = Matter.Engine,
        Render = Matter.Render,
        World  = Matter.World,
        Bodies = Matter.Bodies;

    var engine = Engine.create();

    var render = Render.create({
        element: document.body,
        engine: engine
    });

    var boxA = Bodies.rectangle(400,200,80,80);
    var boxB = Bodies.rectangle(450, 540, 80,80, {isStatic: true});
    var ground = Bodies.rectangle(400, 610, 600, 60, { isStatic: true });

    shapes_array = [boxA, boxB, ground];
    current_box = boxA;

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
        if(event.keyCode == 32) {
            var newbox = Bodies.rectangle(450, 50, 80,80);
            shapes_array.push(newbox)
            World.add(engine.world, newbox);
            current_box = newbox;
        }
    });

    Engine.run(engine);
    Render.run(render);
})()
