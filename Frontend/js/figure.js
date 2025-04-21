export default class Figure {

    constructor(name, position, rotation, document) {
        // Konstanten
        this.stepX = 98;
        this.stepY = 86;
        this.offsetX = -54;
        this.offsetY = -52;
        this.name = name;
        this.document = document;   
        this.calculationPosition = position;
        this.calculationRotation = rotation;

        this.calculate();
        this.createHTMLelement();
    }

    calculate() {
        this.position = {
            "X": Math.ceil(this.calculationPosition.X * this.stepX + this.offsetX), 
            "Y": Math.ceil(this.calculationPosition.Y * this.stepY + this.offsetY)
        };
        this.rotation = `rotateX(${this.calculationRotation.rotX}deg)rotateY(${this.calculationRotation.rotY}deg)rotateZ(${this.calculationRotation.rotZ}deg)`;
    }

    createHTMLelement() {
        // kreiere das HTML-Element
        this.img = this.document.createElement('img');
        this.img.id = this.name;
        this.img.src = `images/${this.name}.svg`;
        this.img.style.shapeRendering = 'crispEdges';
        this.img.style.position = 'absolute';
        this.img.style.left = this.position.X + (this.calculationPosition.Y % 2 === 0 ? 0 : 49) + 'px';
        this.img.style.top = this.position.Y + 'px';
        this.img.style.transform = this.rotation;    
        this.img.className = 'dynamic-image';

        // füge das HTML-Element zum Container hinzu
        this.container = document.getElementById('Brett');
        this.container.appendChild(this.img);
    }

    get_HTMLelement() {
        return this.img;
    }

    get_CalculationPosition() {
        return this.calculationPosition;
    }  

    get_CalculationRotation() {    
        return this.calculationRotation;        
    }

    removeImg() {
        this.img.remove();
    }

    refresh_figure() {
        this.removeImg();
        this.createHTMLelement();
    }

    describe() {
        console.log(`Figure: ${this.name}, Position: (${this.position.X}, ${this.position.Y}), Rotation: ${this.rotation}`);      
    }

    // Bewegungen: 
    rotate(direction) {
        this.calculationRotation.rotX += direction.rotX;
        this.calculationRotation.rotY += direction.rotY;
        this.calculationRotation.rotZ += direction.rotZ;
        this.calculate();
        this.refresh_figure();
    }

    move(direction) {
        var correction = 0;
        if (direction.X === +1 && direction.Y === +1 && this.calculationPosition.Y % 2 === 0) {
            correction = -1};
        if (direction.X === -1 && direction.Y === -1 && this.calculationPosition.Y % 2 === 1) {
            correction = +1};
        if (direction.X === -1 && direction.Y === +1 && this.calculationPosition.Y % 2 === 1) {
            correction = +1};
        if (direction.X === +1 && direction.Y === -1 && this.calculationPosition.Y % 2 === 0) {
            correction = -1};
    
        this.calculationPosition.X += direction.X + correction;
        this.calculationPosition.Y += direction.Y;   
        this.calculate();
        this.refresh_figure();
    }

}

