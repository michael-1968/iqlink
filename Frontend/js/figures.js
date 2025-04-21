import Figure from './figure.js';
import LocalStorageHandler from './localStorageHandler.js';
import {filename} from './dataexchange.js'


class Figures {
    constructor(){
        this.localStorageHandler = LocalStorageHandler;
        this.showProgressStorage = new Map();
//        this.nameOfLastAddedFigure = '';
        return Figures.instance;
    }

    addFigure(fx){
        this.localStorageHandler.updateEntry(fx);
//        this.nameOfLastAddedFigure = fx.name;
    }

    removeFigure(fx){
        this.localStorageHandler.delete(fx.name);
    }

    getFigure(name) {
        return this.localStorageHandler.figure(name);
    }

    clearMemory() {
        console.log("Figures: clearMemory");
        this.localStorageHandler.deleteAll();
    }

    showFigures(dx) {
        this.localStorageHandler.get_AsArray().forEach((fx, name) => {
//            console.log("Figures: showFigures - fx: ", fx, fx.name);
            fx = new Figure(fx.name, fx.calculationPosition, fx.calculationRotation, dx);    
        });
    }

    checkFigureMatch(arr, probeFigure) {
        for (const fx of arr) {
            if (
                (fx.name === probeFigure.name) &&
                (fx.position.X === probeFigure.calculationPosition.X) &&
                (fx.position.Y === probeFigure.calculationPosition.Y) &&
                (fx.rotation.rotX === probeFigure.calculationRotation.rotX) &&
                (fx.rotation.rotY === probeFigure.calculationRotation.rotY) &&
                (fx.rotation.rotZ === probeFigure.calculationRotation.rotZ)
                ) {
                return fx;
            }
        };
        return null;
    }

    showProgress(data, dx) {
        const figuresToShowArray = Object.values(data);
        let figuresToShow = figuresToShowArray.reduce((map, item) => {
            map.set(item.name, item);
            return map;
        }, new Map());

//        console.log("Figures-ShowProgress-data: ", figuresToShowArray);
        figuresToShowArray.forEach((item) => {
            let fx = this.showProgressStorage.get(item.name);
            if (fx) {
                let match = this.checkFigureMatch(figuresToShowArray, fx);
                if (match == null) {
//                    console.log("match figure: ", this.checkFigureMatch(figuresToShowArray, fx), figuresToShowArray, fx);
                    fx.calculationPosition = item.position;
                    fx.calculationRotation = item.rotation;
                    fx.calculate();
                    fx.refresh_figure();
                }
//                console.log("refresh figure: ", fx);
            } else {
                fx = new Figure(item.name, item.position, item.rotation, dx);   
                this.showProgressStorage.set(item.name, fx);
//                console.log("New figure: ", fx);
            }
//        console.log("Figures-ShowProgress: ", item, item.name, item.position, item.rotation)
        });

        this.showProgressStorage.forEach((item) => {   
            let fx = figuresToShow.get(item.name);
            if (!fx) {
                item.removeImg();
                this.showProgressStorage.delete(item.name);
            }
        });        
    }

    getFigureMemoryAsJson() {
        const arr = [];
        for (const [key, value] of this.localStorageHandler.get_AsMap()) {
            arr.push({
                name: value.name,
                position: value.calculationPosition,
                rotation: value.calculationRotation,
            });
        }
        var ox = arr.reduce((obj, item, id) => {
            obj[id] = item; // Verwende `id` als Schlüssel
            return obj;
        }, {});

        return ox;
    }

    // Funktion zum Entfernen aller Figuren
    removeImages(dx) {
        const images = dx.querySelectorAll('img');
        images.forEach(image => {
            if (filename(image.src) != "Brett") {
                if (!(image.classList.contains('figur'))) {
                    image.remove();
                }
            }
        });
    }
}

const figures = new Figures();

export default figures;

