document.addEventListener('DOMContentLoaded', async (event) => {
    const joystick = document.getElementsByClassName('joystick')[0];
    const stick = document.getElementsByClassName('stick')[0];

    let joystickRadius = parseInt(window.getComputedStyle(joystick).width)/2;
    let stickRadius = parseInt(window.getComputedStyle(stick).width)/2;
    let radius = joystickRadius - stickRadius;
    console.log("radius:" + radius);
    let dragging = false;
    let animationFrameId = null;

    // Initialize WebSocket connection
    let socket = new WebSocket("ws://[RASPBEERY IP]]/direction");
    /*
    socket.addEventListener("open", () => {
        socket.send("Hello Server!"); 
    });
    */
    const resetStickPosition = () => {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        stick.style.top = '${radius}px';
        stick.style.left = '${radius}px';

        moveStick(0, 0);
    };

    const moveStick = (x, y) => {
        stick.style.top = `${y + radius}px`;
        stick.style.left = `${x + radius}px`;

        console.log("x: " + x + ", y:" + y);
        // Send coordinates via WebSocket
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(x)
            socket.send(y)
        }
    };

    const handleMovement = (clientX, clientY) => {
        const rect = joystick.getBoundingClientRect();
        let x = clientX - rect.left - joystickRadius; // Offset to center (range: -75 to 75)
        let y = clientY - rect.top - joystickRadius;

        //console.log("rect top" + rect.top + " rect left" + rect.left + " rect right" + rect.right)

        // Constrain values between -75 and 75
        x = Math.max(-radius, Math.min(x, radius));
        y = Math.max(-radius, Math.min(y, radius));

        let current_radius = Math.sqrt(x*x + y*y); 
        if (current_radius > radius) {
            const scale = radius / current_radius;
            x *= scale;
            y *= scale;
        }

        // Request a frame update to move the stick
        if (!animationFrameId) {
            animationFrameId = requestAnimationFrame(() => {
                moveStick(x, y);
                animationFrameId = null; // Reset after rendering
            });
        }
    };
    
    // What should the joystick do?
    // 1. Enable dragging of joystick when mousedown/touchdown
    stick.addEventListener('mousedown', (e)=>{
         dragging = true;
     })
    // 2. Disable dragging of joystick when mousedown/touchdown
     document.addEventListener('mouseup', ()=>{
        console.log("STOPPED / RELEASED")
         if(dragging){
             dragging = false;
             resetStickPosition();
         }
     })
    // // 3. Update joystick position when mousemove/touchmove
     document.addEventListener('mousemove', (e)=>{
         if(dragging){
             handleMovement(e.clientX, e.clientY);
         }
     })
    
     // 1. Enable dragging of joystick when mousedown/touchdown
    stick.addEventListener('touchstart', (e)=>{
        dragging = true;
    })
    // 2. Disable dragging of joystick when mousedown/touchdown
    document.addEventListener('touchend', ()=>{
        console.log("TOUCH HAS ENDED");
        if(dragging){
            dragging = false;
            resetStickPosition();
        }
    })
    // 3. Update joystick position when mousemove/touchmove
    document.addEventListener('touchmove', (e)=>{
        e.preventDefault();
        if(dragging){
            handleMovement(e.touches[0].clientX, e.touches[0].clientY);
        }
    }, { passive:false })
    resetStickPosition();
});

// Set up Server
// python -m http.server 8000
// in cmd do ipconfig to get IPv4
// http//[IPv4 Address]:8000