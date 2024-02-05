//variables
const framework = 'Django';
const language = 'Python';
alert(framework + `is writen in ${language}`);

// conditionals
const name = 'Ben';
let benCount = 0;
if ( name === 'Ben'){
  benCount = 1;
};
alert('There is' + `${benCount} ` + 'Ben');  // just an allert

// arrays
const fruit = ['Apple', 'Banana']
fruit.push('Cherry')  // append 'Cherry' to the end of the `fruit` list

const fruitCount = {Apple: 0, 'Banana': 1}
fruitCount.Cherry = 2  // add new item to object
fruitCount['Cherry'] = 2  // is equivalent

const myFruit = 'Cherry'
fruitCount[myFruit] = 2 // is also equivalent


// scopes
const theNumber = 1
let firstName = 'Ben'

if (theNumber === 1) {
  let firstName = 'Leo'
  alert(firstName) // Leo
}

alert(firstName) // Ben