/*var url = 'http://newsapi.org/v2/top-headlines?' +
          'country=us&' +
          'apiKey=api_key_get_from_news_api';

var req = new Request(url);
var a = 0;

fetch(req)
    .then((res) => res.json())
    .then((data) => {
      //show the first news as example
      document.getElementById('apiReturn').innerHTML += ("<h3>" + data.articles[a].title + "</h3>" + "<h5>" + data.articles[a].description + "</h5>" + data.articles[a].content);
    });

function moreNews() {
  a += 1;
  if (a < data.articles.length) {
    document.getElementById('apiReturn').innerHTML += ("<h3>" + data.articles[a].title + "</h3>" + "<h5>" + data.articles[a].description + "</h5>" + data.articles[a].content);
  };
};
*/

const json = '{"status": "ok", "totalResults": 38, "articles": [{"source": {"id": null, "name": "YouTube"}, "author": null, "title": "DeVonta Smith vs. Jaylen Waddle: Which Alabama WR is the better NFL prospect? | Get Up - ESPN", "description": "Desmond Howard and Ryan Clark discuss Alabama Crimson Tide WR Jaylen Waddle being cleared to practice and what it could mean if he plays in the College Football", "url": "https://www.youtube.com/watch?v=zxoIRPgNMu8", "urlToImage": "https://i.ytimg.com/vi/zxoIRPgNMu8/maxresdefault.jpg", "publishedAt": "2021-01-06T15:25:10Z", "content": "Alabama has had some famed pass catchers over the years. Don Hutson is considered the first great wide receiver, modernizing the position in the 1930s. Dennis Homan and Ray Perkins starred on some great teams in the 1960s. Ozzie Newsome was a Hall of Fame tight end in the ‘70s. But it wasn’t until the Nick Saban Era that Alabama began to stockpile large quantities of elite talent at wide receiver. What started with Julio Jones continued with Amari Cooper, Calvin Ridley and others. There are eight Alabama wideouts on NFL rosters this season. Alabama now has achieved peak wideout weaponry. When a team can lose two top-15 NFL draft picks (Henry Ruggs and Jerry Jeudy), then have a third star break his ankle midway through the season (Jaylen Waddle) and still have the best receiver in the nation?"}]}';
const data = JSON.parse(json);

//console.log(obj.status);
document.getElementById('apiReturn').innerHTML += ("<h3>" +data.articles[0].title + "</h3>" + "<h5>" + data.articles[0].description + "</h5>" + data.articles[0].content);

function moreNews() {
  alert("This is an example! Register for a free APIKey on newsapi.org")
}
