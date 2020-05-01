var fs = require("fs");
const process = require('process')
const solc = require('solc');

const verifierCon = process.argv[2]

// -----Compile contract-----
function compile(){
    const source = fs.readFileSync(verifierCon, 'UTF-8');
    let jsonContractSource = JSON.stringify({
        language: 'Solidity',
        sources: {
            [verifierCon]: {
                content: source,
            },
        },
        settings: {
            outputSelection: {
                '*': {
                    '*': ['abi', "evm.bytecode"],
                },
            },
            "optimizer": {
                // disabled by default
                "enabled": true,
            }
        },
    });
    writeArti(JSON.parse(solc.compile(jsonContractSource)))
}


function writeArti(jsonInterface){
    fs.writeFile('verifier.abi', JSON.stringify(jsonInterface.contracts[verifierCon]["Verifier"].abi), function (err,data) {
        if (err) {
          return console.log(err);
        }})
    fs.writeFile('verifier.bin', jsonInterface.contracts[verifierCon]["Verifier"].evm.bytecode.object, function (err,data) {
        if (err) {
          return console.log(err);
        }});
}

compile()