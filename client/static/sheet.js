window.onload = () => {
    const data = [
        ['', 'Ford', 'Tesla', 'Toyota', 'Honda'],
        ['2017', 10, 11, '2017-01-01', 13],
        ['2018', 20, 11, '2018-12-12', 13],
        ['2019', 30, 15, '2019-30-30', 13]
    ];

    const container = document.getElementById('sheet');
    const hot = new Handsontable(container, {
        data: data,

        rowHeaders: true,
        colHeaders: ['A', 'B', 'C','D','E'],
        filters: true,
        dropdownMenu: true,
        outsideClickDeselects: false,
        licenseKey: 'non-commercial-and-evaluation'
    });
    window.Handsontable = Handsontable;
    window.hot = hot;

    setTimeout(()=>window.postMessage({
        type: "TFXI_HANDSHAKE",
        command: '',
        args: [''],
        tfx: '',
        hint: 'format [cells] as [formatType]',
        sample: 'format A1:A3 date',
        voiceContext: []}, "*"), 1000);
    window.addEventListener("message", function (event) {
        // We only accept messages from ourselves
        if (event.source !== window)
            return;

        if (event.data.type && (event.data.type === "FROM_SANAZ")) {
            console.log("App received: " + JSON.stringify(event.data));
            if(tfx.hasOwnProperty(event.data.command)){
                console.log(event.data)
                tfx[event.data.command](...event.data.params)
            }
        }
    }, false);
};

const tfx = {};

window.tfx = tfx;

function getColumnIndex(columnLetter) {
    const charCode = columnLetter.charCodeAt(0);
    const charCodeForA = 'a'.charCodeAt(0);
    const charCodeForCapitalA = 'A'.charCodeAt(0);
    return charCode >= charCodeForA ? charCode - charCodeForA : charCode - charCodeForCapitalA;
}

function getRowIndex(rowLetter) {
    return parseInt(rowLetter) - 1;
}

function parseCell(cell) {
    let [columnLetter, ...rowLetter] = cell;
    rowLetter = rowLetter.join('');
    return [getRowIndex(rowLetter), getColumnIndex(columnLetter)];
}

function isRange(element) {
    return element.indexOf(':') > 0;
}

function parseRange(element) {
    let start, end;
    if (isRange(element)) {
        [start, end] = element.split(':');
    } else {
        start = element;
        end = element;
    }
    start = parseCell(start);
    end = parseCell(end);
    return [...start, ...end];
}

function parseSelection(selection) {
    return selection.split(',').map(element => parseRange(element));
}

tfx.select = selection => {
    // e.g. tfx.select('A1:B2,B3,D2:E2')
    console.log('selection func')
    console.log(selection)
    if(selection.element.toLowerCase()==='column'){
        console.log('im a columns')
        let name = +selection.name;
        if(isNaN(name)){
            console.log(selection.name)
            window.hot.selectColumn(selection.name)
        }else{
            window.hot.selectColumns(name)
        }
    } else
    if(selection.element.toLowerCase()==='row'){
        console.log('im a row')
        let name = +selection.name;
        if(isNaN(name)){
            window.hot.selectRows(selection.name)
        }else{
            window.hot.selectRows(name)
        }
    }

};

tfx.format = (selection, {type}) => {
    if (!selection) {
        return;
    }
    console.log(selection)
    console.log(type)
    // selection = selection === 'current' ? window.hot.getSelected() : parseSelection(selection);
    const typeConfigs = {
        'date': {
            correctFormat: true,
            dateFormat: 'MM/DD/YYYY'
        },
        'text': {
            validator: undefined
        }
    };
    if(selection.element.toLowerCase()==='column'){
        console.log('im a columns')
        let name = +selection.name;
        if(isNaN(name)){
            console.log(selection.name)
            window.hot.selectColumn(selection.name)
        }else{
            window.hot.selectColumns(name)
        }
    } else
    if(selection.element.toLowerCase()==='row'){
        console.log('im a row')
        let name = +selection.name;
        if(isNaN(name)){
            window.hot.selectRows(selection.name)
        }else{
            window.hot.selectRows(name)
        }
    }
    for (const {from, to} of window.hot.getSelectedRange()) {
        for (let row = from.row; row <= to.row; row++) {
            for (let column = from.col; column <= to.col; column++) {
                window.hot.setCellMetaObject(row, column, {
                    validator: type,
                    renderer: type,
                    editor: type,
                    ...typeConfigs[type]
                });
            }
        }
    }

    window.hot.validateCells();
    window.hot.render();
};
