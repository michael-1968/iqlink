class LocalStorageHandler {

    constructor() {
        if (LocalStorageHandler.instance) {
            return LocalStorageHandler.instance;
        }
        this.saveTag = 'figures';
        LocalStorageHandler.instance = this;
    }

    static getInstance() {
        if (!LocalStorageHandler.instance) {
            LocalStorageHandler.instance = new LocalStorageHandler();
        }
        return LocalStorageHandler.instance;
    }

    save(map) {
//        console.log("save-stringified: ", JSON.stringify(Array.from(map)));
        localStorage.setItem(this.saveTag, JSON.stringify(Array.from(map)));
    }

    saveJsonFormattedData(jsondata) {
//        console.log("saveJsonFormattedData: ", jsondata);
//        console.log("saveJsonFormattedData-stringified: ", JSON.stringify(jsondata));
        localStorage.setItem(this.saveTag, JSON.stringify(jsondata));
    }

    updateEntry(figure) {
        let key = figure.name;
        let figuresString = localStorage.getItem(this.saveTag);
        let mx = new Map(JSON.parse(figuresString));
        mx.set(key, figure);
        this.save(mx);
    }

    delete(name) {      
        let figuresString = localStorage.getItem(this.saveTag);
        let mx = new Map(JSON.parse(figuresString));
        mx.delete(name);
        this.save(mx);
    }

    deleteAll() {
        let map = new Map();
        localStorage.setItem(this.saveTag, JSON.stringify(Array.from(map)));
    }

    figure(name) {
        let figuresString = localStorage.getItem(this.saveTag);
        let mx = new Map(JSON.parse(figuresString));
        return mx.get(name);
    }

    get_AsMap() {
        let figuresString = localStorage.getItem(this.saveTag);
        return new Map(JSON.parse(figuresString));
    }

    get_AsArray() {
        return Array.from(this.get_AsMap().values());
    }

}

export default LocalStorageHandler.getInstance();
