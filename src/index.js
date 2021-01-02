import lampix from '@lampix/core';

var url = 'http://newsapi.org/v2/top-headlines?' +
          'country=us&' +
          'apiKey=c05706d6b25d48c581ecb20476f0884f';
var req = new Request(url);
fetch(req)
    .then(function(response) {
        console.log(response.json());
    })
