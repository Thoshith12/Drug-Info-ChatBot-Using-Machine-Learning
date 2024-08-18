let a
var apiKey = "6wQGedfigIKwuiQTnYUr9y4RnX3FXH58RLZseQdy";
var display = []
var display = document.querySelector('.display')
let dropdownOptions = document.querySelector('#dropdown-options');
let dropdown = document.querySelector(".dropdown-header");
let drug;
dropdownOptions.classList.toggle('show')
let type = '0'
function test(text) {
    display.innerHTML = `<div class="loader"></div>`
    toggleDropdown();
    dropdown.innerHTML = text;
    drug = document.querySelector('#drug');
    $.ajax({
        url: "https://api.fda.gov/drug/event.json?api_key=" + apiKey + "&search=" + drug.value,
        dataType: "json",
        type: 'GET',

        success: function (data, err) {
            let drugt = []
            display.innerHTML = '<h1 id="react">Some Medicinal Products are:<h1> '
            for (var i = 0; i < 100; i++) {
                if (data.results[0].patient.drug[i].medicinalproduct) {
                    var activesubstance = (data.results[0].patient.drug[i].medicinalproduct)
                }
                if (data.results[0].patient.drug[i].openfda) {
                    var brand_name = (data.results[0].patient.drug[i].openfda.brand_name[0])
                }
                if (data.results[0].patient.drug[i].openfda) {
                    var drug = (data.results[0].patient.drug[i].openfda.generic_name[0])
                }
                if (data.results[0].patient.drug[i].openfda) {
                    var manufacturer_name = (data.results[0].patient.drug[i].openfda.manufacturer_name[0])
                }
                if (data.results[0].patient.drug[i].openfda) {
                    var product_type = (data.results[0].patient.drug[i].openfda.product_type[0])
                    if (drugt.includes(drug)) {
                    }
                    else {
                        drugt += drug
                        display.innerHTML += `<span class="info"><h6>Medicinalproduct:${activesubstance}</h6><h5>Brand Name:${brand_name}</h5><h5>Generic Name:${drug}</h5><h5>Manufacturer Name:${manufacturer_name}</h5><h5>Prescription Type:${product_type}</h5></span>`
                    }
                }
            }
        }
    })
}

function reactions(text) {
    display.innerHTML = `<div class="loader"></div>`
    toggleDropdown();
    dropdown.innerHTML = text;
    drug = document.querySelector('#drug');
    $.ajax({
        url: "https://api.fda.gov/drug/event.json?api_key=" + apiKey + "&search=" + drug.value + "&count=patient.reaction.reactionmeddrapt.exact",
        dataType: "json",
        type: 'GET',

        success: function (data, err) {
            console.log(this.url, data)
            display.innerHTML = `<h1 id="react">Possible drug reactions based on FDA testing:-<h1>`

            for (var i = 0; i < 1000; i++) {
                //store side effect
                var result = (data.results[i].term)
                var number = (data.results[i].count)
                if (result == 'DRUG INEFFECTIVE') {
                    result = "DRUG INEFFECTIVE"
                } else if (result === 0) {
                    alert("Try another search")
                } else {
                    var newDiv = '<div class="box"><a href="https://www.google.com/search?q=what is ' + result + '  drug reaction">' + '<p>Reaction: ' + result + '</p><p>' + 'People Effected:' + number + '</p><a></div>'
                    $('.display').append(newDiv)
                }
            }
        }
    })
}

async function drugs(drug, rxcui) {
    $.ajax({
        url: "https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=" + rxcui + "&sources=DrugBank",
        dataType: "json",
        type: 'GET',
        success: function (data, err) {
            if (a != 2) {
                display.innerHTML = `<h2>Possible drug intereactions based on RXCUI testing:-<h2>`
                a = 2
            }
            // console.log(this.url, data)
            let interactions = [];
            let urt = []
            for (var i = 0; i < 4; i++) {
                if (data.interactionTypeGroup) {
                    interactions += `<p>${data.interactionTypeGroup[0].interactionType[0].interactionPair[i].description}</p><br>`
                    // error throwback for dugs like  NATROBA
                    urt += `<p>${data.interactionTypeGroup[0].interactionType[0].interactionPair[i].interactionConcept[1].sourceConceptItem.name}</p><p>${data.interactionTypeGroup[0].interactionType[0].interactionPair[i].interactionConcept[1].sourceConceptItem.url}</p><br>`
                    // <h3>Drug url's are:<br><br>${urt}</h3>
                }
            }
            if (data.interactionTypeGroup) {
                display.innerHTML += `<article><h1>Generic Name:${drug}</h1>
<h2>Drug Description:${data.interactionTypeGroup[0].interactionType[0].comment}</h2>
<h3>Possible Drug Interactions are:<br><br>${interactions}</h3></article>`
            }
            else {
                display.innerHTML += `<article><h2>RXNAV Disclaimer:${data.nlmDisclaimer}</h2><h1>Error finding drug Interactions,please comback after sometime</h1></article>`
            }
        }
    })
}

function interaction(text) {
    display.innerHTML = `<div class="loader"></div>`
    toggleDropdown();
    dropdown.innerHTML = text;
    drug = document.querySelector('#drug');
    window.location.href = '#enter';
    $(".display").html("")

    $.ajax({
        url: "https://api.fda.gov/drug/event.json?api_key=" + apiKey + "&search=" + drug.value,
        dataType: "json",
        type: 'GET',

        success: function (data, err) {
            // console.log(this.url, data)
            let drugt = []
            a = 1
            for (var i = 0; i < 10; i++) {
                if (data.results[0].patient.drug[i]) {
                    if (data.results[0].patient.drug[i].openfda) {
                        drug = (data.results[0].patient.drug[i].openfda.generic_name[0])
                        if (data.results[0].patient.drug[i].openfda.rxcui) {
                            var rxcui = (data.results[0].patient.drug[i].openfda.rxcui[0])
                        }
                        if (drugt.includes(drug)) {
                            // console.log('hi', drugt)
                        } else {
                            drugt += drug
                            drugs(drug, rxcui)
                            // console.log('hii', drugt)
                        }

                    }
                }
            }
        }
    })
}

function prescription(text) {
    display.innerHTML = `<div class="loader"></div>`
    toggleDropdown();
    dropdown.innerHTML = text;
    drug = document.querySelector('#drug');
    $.ajax({
        url: "https://api.fda.gov/drug/label.json?search=" + drug.value + "&count=openfda.product_type.exact",
        dataType: "json",
        type: 'GET',

        success: function (data, err) {
            var result = (data.results[0].term)
            console.log(result)
            display.innerHTML = `<span class="type"><h1>Prescription Type :<br><br> ${result}</h1></span>`

        }

    })

}

function toggleDropdown() {
    dropdownOptions.classList.toggle('show')
}