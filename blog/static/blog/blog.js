// //variables
// const framework = 'Django';
// const language = 'Python';
// alert(framework + `is writen in ${language}`);

// // conditionals
// const name = 'Ben';
// let benCount = 0;
// if ( name === 'Ben'){
//   benCount = 1;
// };
// alert('There is' + `${benCount} ` + 'Ben');  // just an allert

// // arrays
// const fruit = ['Apple', 'Banana']
// fruit.push('Cherry')  // append 'Cherry' to the end of the `fruit` list

// const fruitCount = {Apple: 0, 'Banana': 1}
// fruitCount.Cherry = 2  // add new item to object
// fruitCount['Cherry'] = 2  // is equivalent

// const myFruit = 'Cherry'
// fruitCount[myFruit] = 2 // is also equivalent


// // scopes
// const theNumber = 1
// let firstName = 'Ben'

// if (theNumber === 1) {
//   let firstName = 'Leo'
//   alert(firstName) // Leo
// }

// alert(firstName) // Ben

// console logs
// console.time('myTimer')
// console.count('counter1')
// console.log('A normal log message')
// console.warn('Warning: something bad might happen')
// console.error('Something bad did happen!')
// console.count('counter1')
// console.log('All the things above took this long to happen:')
// console.timeEnd('myTimer')

// // functions, arguments in functions dont need to be passed they are optional by default
// function addNumbers(a, b) {
//   return a+b;
// }

// const result = addNumbers(3,4)
// console.log(result)

// function sayHello(name) {
//   if (name === undefined){
//     console.log("Hello no name");
//   } else {
//     console.log(`Hello ${name}`);
//   }
// }

// sayHello() // name is undefined
// sayHello('Lily');

// assign function to variables
// const sayHello = function(name) {
//   if (name === undefined){
//     console.log('Hello no name')
//   } else {
//     console.log(`Hello ${name}`)
//   }
// }

// sayHello("Mark")

// anonymous or arrow functions
// const sayHello = (name) => {
//   if (name === undefined){
//     console.log('Hello no name')
//   } else {
//     console.log(`Hello ${name}`)
//   }
// }

// // lambda functions
// const doubler = (x) => {return x*2}
// console.log(doubler(2))

// // or
// const doubler = x => x*2

// callback functions
// function showAnAlert() {
//   alert('Timeout finished.')
// }

// setTimeout(showAnAlert, 2000)

// const name = 'Ben'

// setTimeout(() => {
//     sayHello(name)
//   }, 2000
// )


// function sayHello(yourName) {
//   if (yourName === undefined) {
//       console.log('Hello, no name')
//   } else {
//        console.log('Hello, ' + yourName)
//   }
// }

// const yourName = 'Your Name'  // Put your name here

// console.log('Before setTimeout')

// setTimeout(() => {
//     sayHello(yourName)
//   }, 2000
// )

// console.log('After setTimeout')

// loops
// for
// for (let i=0; i<10; i+=1){
//   console.log(i)
// }

// while
// let i=0
// while(i<10){
//   console.log(i);
//   i += 1
// }

// do while loop
// let i = 10
// do {
//   console.log(i)
//   i += 1
// } while(i < 10)

// // iterating though arrays
// // for each
// const numbers = [0,1,2,3,4,5,6]

// numbers.forEach((value)=>{
//   console.log(value)
// })
// // map
// const doubled = numbers.map(value => value *2)
// console.log(doubled)


// // classes // inheritance
// class Greeter {
//   constructor (name) {
//     this.name = name
//   }

//   getGreeting () {
//     if (this.name === undefined) {
//       return 'Hello, no name'
//     }

//     return 'Hello, ' + this.name
//   }

//   showGreeting (greetingMessage) {
//     console.log(greetingMessage)
//   }

//   greet () {
//     this.showGreeting(this.getGreeting())
//   }
// }

// const g = new Greeter('Patchy')  // Put your name here if you like
// g.greet()

// // inheritance example
// class DelayedGreeter extends Greeter {
//   delay = 2000

//   constructor (name, delay) {
//     super(name)
//     if (delay !== undefined) {
//       this.delay = delay
//     }
//   }

//   greet () {
//     setTimeout(
//       () => {
//         this.showGreeting(this.getGreeting())
//       }, this.delay
//     )
//   }
// }

// const dg2 = new DelayedGreeter('Patchy 2 Seconds')
// dg2.greet()

// const dg1 = new DelayedGreeter('Patchy 1 Second', 1000)
// dg1.greet()

// promises
function resolvedCallback(data) {
  console.log('Resolved with data ' +  data)
}

function rejectedCallback(message) {
  console.log('Rejected with message ' + message)
}

const lazyAdd = function (a, b) {
  const doAdd = (resolve, reject) => {
    if (typeof a !== "number" || typeof b !== "number") {
      reject("a and b must both be numbers")
    } else {
      const sum = a + b
      resolve(sum)
    }
  }

  return new Promise(doAdd)
}

const p = lazyAdd(3, 4)
p.then(resolvedCallback, rejectedCallback)

lazyAdd("nan", "alsonan").then(resolvedCallback, rejectedCallback)