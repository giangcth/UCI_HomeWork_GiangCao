// from data.js
var tableData = data;

// Get a reference to the table body
var tbody = d3.select("tbody");


// Use d3 to update each cell's text with
// // UFO Sightings report values (date, City, State, Country, Shape, Duration, Comments)
tableData.forEach((UFOSighting) => {
    var row = tbody.append("tr");
    Object.entries(UFOSighting).forEach(([key, value]) => {
        var cell = row.append("td");
        cell.text(value);
        });
});

// Map Arrays to hold unique attribute list
var UFOShapeList = tableData.map(tableData => tableData.shape).filter((value, index, self) => self.indexOf(value) === index);
var UFOCityList = tableData.map(tableData => tableData.city).filter((value, index, self) => self.indexOf(value) === index);
var UFOStateList = tableData.map(tableData => tableData.state).filter((value, index, self) => self.indexOf(value) === index);
var UFODateList = tableData.map(tableData => tableData.datetime).filter((value, index, self) => self.indexOf(value) === index);

// Console.log the UFO Sightings data from data.js
console.log(UFOShapeList);
console.log(UFOShapeList.length);
console.log(UFOCityList);
console.log(UFOCityList.length);
console.log(UFOStateList);
console.log(UFOStateList.length);
console.log(UFODateList);
console.log(UFODateList.length);

// // Select the button
var button = d3.select("#filter-btn");

// Select the form
var form = d3.select("#form");

button.on("click", runEnter);
form.on("submit",runEnter);

// Create and Complete the event handler function for Date Form
function runEnter() {
    // clears the data of the current table        
    tbody.html("");
    // Prevent the page from refreshing
    d3.event.preventDefault();
    // print "You have just clicked the 'Filter Table' on console, for testing
    console.log("You have just clicked the ' Date Time Filter Button'.");
    // Select the input element and get the raw HTML node
    var inputElementDate = d3.select("#datetime");
    var inputElementCity = d3.select("#cityname");
    var inputElementState = d3.select("#statename");
    var inputElementCountry = d3.select("#countryname");
    var inputElementShape = d3.select("#shapename");

    // Get the value property of the input element
    var inputValueDate = inputElementDate.property("value").toLowerCase();
    var inputValueCity = inputElementCity.property("value").toLowerCase();
    var inputValueState = inputElementState.property("value").toLowerCase();
    var inputValueCountry = inputElementCountry.property("value").toLowerCase();
    var inputValueShape = inputElementShape.property("value").toLowerCase();
    
    console.log(inputValueDate);
    console.log(inputValueCity);
    console.log(inputValueState);
    console.log(inputValueCountry);
    console.log(inputValueShape);

        
    var filteredData = tableData.filter(UFO => UFO.datetime === inputValueDate ||
                                        UFO.city === inputValueCity ||
                                        UFO.state === inputValueState ||
                                        UFO.country === inputValueCountry ||
                                        UFO.shape === inputValueShape       
        );

    console.log(filteredData);

    // Use d3 to update each cell's text with
    // // UFO Sightings report values (date, City, State, Country, Shape, Duration, Comments)
    filteredData.forEach((UFOSighting) => {
    var row = tbody.append("tr");
    Object.entries(UFOSighting).forEach(([key, value]) => {
        var cell = row.append("td");
        cell.text(value);
        });
    });
};

