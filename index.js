//import lampix from '@lampix/core';

//import './styles.css';
//import randomColor from './randomColor';
//import handleObjectClassified from './handleObjectClassified';

var url = 'http://newsapi.org/v2/top-headlines?' +
          'country=us&' +
          'apiKey=c05706d6b25d48c581ecb20476f0884f';

var req = new Request(url);

fetch(req)
    .then((res) => res.json())
    .then((data) => {
      //show the first news as example
      document.getElementById('apiReturn').innerHTML += ("<h3>" +data.articles[0].title + "</h3>" + "<h5>" + data.articles[0].description + "</h5>" + data.articles[0].content);
      /*
      for (var a in data.articles) {
        console.log(data.articles[a].title);
        console.log(data.articles[a].description);
        //alert(data.articles[a].content);
        document.getElementById('apiReturn').innerHTML += (data.articles[a].description + "<br><br>");
      }*/
    });

/*
fetch(req)
    .then(function(response) {
        //console.log(response.json());
        //alert(response.json());
        var data = JSON.stringify(response.json());
        //alert(data.length);
        console.log(data);
        for (var key in data) {
          if (data.hasOwnProperty(key)) {
            console.log(data[key]);
          }
        }
        ///*
        for(var i = 0; i < data.length; i++) {
          var obj = data[i];
          console.log(obj);
        }
        //*/
        /*
        data.forEach(obj => {
          Object.entries(obj).forEach(([key, value]) => {
            console.log('${key} ${value}');
          });
          console.log('--------------------------------');
        });
        */
    //});
//*/
/*
const initializeNNC = () => {
  const nncElement = document.getElementsByClassName('nnc')[0];
  const nncBounds = nncElement.getBoundingClientRect();
  const nncRecognizedClassElement = document.getElementsByClassName('nnc-recognized-class')[0];

  // All Lampix classifiers return a list of recognized objects
  // NNClassifier only recognizes one at a time, hence expecting
  // an array with one element and destructuring it
  const nncCallback = ([recognizedObject]) => {
    nncRecognizedClassElement.textContent = `Recognized: ${recognizedObject.classTag}`;

    if (Number(recognizedObject.classTag) === 1) {
      // Change border color on each new detection
      nncElement.style.borderColor = randomColor();
    } else {
      // Go back to white if object no longer there
      nncElement.style.borderColor = '#FFFFFF';
    }
  };

  const nncFruitsWatcher = {
    name: 'NeuralNetworkClassifier',
    shape: lampix.helpers.rectangle(
      nncBounds.left,
      nncBounds.top,
      nncBounds.width,
      nncBounds.height
    ),
    params: {
      neural_network_name: 'fruits'
    },
    onClassification: nncCallback
  };

  lampix.watchers.add(nncFruitsWatcher);
};

const initializeMBS = () => {
  const mbsElement = document.getElementsByClassName('mbs')[0];
  const mbsBounds = mbsElement.getBoundingClientRect();

  // Associate one class to one color
  const classColorMap = {};

  const onClassification = (classifiedObjects) => classifiedObjects.forEach((classifiedObject) => {
    let color = classColorMap[classifiedObject.classTag];

    if (!color) {
      color = randomColor();
      classColorMap[classifiedObject.classTag] = color;
    }

    handleObjectClassified(classifiedObject, color);
  });

  const onLocation = (locatedObjects) => {
    // This step fires before onClassification!
    console.log(locatedObjects);
  };

  const mbsFruitsWatcher = {
    name: 'MovementBasedSegmenter',
    shape: lampix.helpers.rectangle(
      mbsBounds.left,
      mbsBounds.top,
      mbsBounds.width,
      mbsBounds.height
    ),
    params: {
      neural_network_name: 'fruits'
    },
    onLocation,
    onClassification
  };

  lampix.watchers.add(mbsFruitsWatcher);
};

initializeNNC();
initializeMBS();
*/
