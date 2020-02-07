var request = require('request');
var cheerio = require('cheerio');
var fs = require('fs');
var CronJob = require('cron').CronJob;
var weekName = getWeekName();
var interval = 5;

function getWeekName() {
    var originalTime = (new Date()).getTime();
    var startDay = new Date()
    startDay.setDate(startDay.getDate() - startDay.getDay());
    var endDay = new Date()
    endDay.setDate(endDay.getDate() + (6 - endDay.getDay()))
    var startDate = (startDay.getDate()<10)?"0"+startDay.getDate():startDay.getDate();
    var endDate = (endDay.getDate()<10)?"0"+endDay.getDate():endDay.getDate();
    var startMonth = ((startDay.getMonth() + 1)<10)?"0"+(startDay.getMonth() + 1):(startDay.getMonth() + 1);
    var endMonth = ((endDay.getMonth() + 1)<10)?"0"+(endDay.getMonth() + 1):(endDay.getMonth() + 1);
    var weekName = "" + startDay.getFullYear() + startMonth + startDate + "-" +
    endDay.getFullYear() + endMonth + endDate;
    return weekName;
}

var job = new CronJob('*/'+interval+' * * * * *', function () {
    if (!fs.existsSync('./tempPaths.json')) {
        var obj = JSON.parse(fs.readFileSync('./pathsFinal.json', 'utf8'));
        fs.writeFileSync('./tempPaths.json', JSON.stringify(obj, null, 4));
    }
    if (!fs.existsSync('./results/'+weekName)){
        fs.mkdirSync('./results/'+weekName)
    }
    if (!fs.existsSync('./results/'+weekName+'/faltantes' + weekName + '.json')) {
        fs.writeFileSync('./results/'+weekName+'/faltantes' + weekName + '.json', JSON.stringify([]));
    }

    var toDo = JSON.parse(fs.readFileSync('./tempPaths.json', 'utf8'));
    console.log("There are "+toDo.length+" paths pending for processing")
    if (toDo.length == 0) {
        fs.unlinkSync("./tempPaths.json")
        job.stop()
    } else {
        var newArray = toDo.slice(1, toDo.length)
        var originalTime = (new Date()).getTime();
        console.log("INFO: retrieving " + toDo[0].path + " - 1 try, on time: " + originalTime)
        getAppList(toDo[0].path, 1, toDo[0], (new Date()).getTime());
        fs.writeFileSync("./tempPaths.json", JSON.stringify(newArray, null, 4));
    }
}, null, true, 'America/Los_Angeles');

function getAppList(pageToVisit, tryy, parent, originalTime) {
    console.log("Info: retrieving of " + pageToVisit + " is about to start")
    var form = { "start": 0, "num": 100, "numChildren": 0, "ipf": 1, "xhr": 1 }
    request.post({ url: pageToVisit, formData: form }, function (error, response, body) {
        if (error && tryy < 11) {
            console.log("ERROR: retrieving " + pageToVisit + " - error: " + error.message)
            var petitionTime = (new Date()).getTime()
            while ((petitionTime - originalTime) < ((interval*1000)/10)) {
                petitionTime = (new Date()).getTime();
            }
            console.log("INFO: retrieving " + element.path + " - " + (tryy + 1) + " try, on time: " + petitionTime)
            getAppList(pageToVisit, tryy + 1, parent, petitionTime)
        }
        else if (response.statusCode !== 200) {
            // the page might not exist due to path creation process (i.e. there are some categories that do not exist for some countries)
            console.log("FAIL: retrieving " + pageToVisit + " - page retrieving error. Status Code: " + response.statusCode)
            // The url is added to unretrieved urls file 
            var obj = JSON.parse(fs.readFileSync('./results/'+weekName+'/faltantes' + weekName + '.json', "utf8"));
            obj[obj.length] = { "element": parent, "statusCode": response.statusCode }
            fs.writeFileSync('./results/'+weekName+'/faltantes' + weekName + '.json', JSON.stringify(obj, null, 4), "utf8")
            console.log("INFO: New toRetrieve task has been added: " + JSON.stringify(obj[obj.length - 1]))
        }
        else if (response.statusCode === 200) {
            // Parse the document body
            console.log("SUCCESS: retrieved " + pageToVisit + " on try: " + tryy)
            var $ = cheerio.load(body);
            var cards = $('.card')
            var links = []
            for (var i = 0; i < cards.length; i++) {
                links[i] = cards[i].children[1].children[1].attribs.href
            }
            // process link list retrieved from url
            processAppList(links, parent);
        } else {
            // the url content was unable to get after 10 tries
            console.log("FAIL: retrieving " + pageToVisit + " - after 10 tries the content was unable to get")
            // The url is added to unretrieved urls file 
            var obj = JSON.parse(fs.readFileSync('./results/'+weekName+'/faltantes' + weekName + '.json', "utf8"));
            obj[obj.length] = { "element": parent }
            fs.writeFileSync('./results/'+weekName+'/faltantes' + weekName + '.json', JSON.stringify(obj, null, 4), "utf8")
            console.log("INFO: New toRetrieve task has been added: " + JSON.stringify(obj[obj.length - 1]))
        }
    });
}

function processAppList(array, element) {

    if (!fs.existsSync('./results/'+weekName+'/toProcess' + weekName + '.json')) {
        fs.writeFileSync('./results/'+weekName+'/toProcess' + weekName + '.json', JSON.stringify([]));
    }
    var toProcess = JSON.parse(fs.readFileSync('./results/'+weekName+'/toProcess' + weekName + '.json', 'utf8'));
    var indice = toProcess.length;
    for (var index = 0; index < array.length; index++) {
        var pageToVisit = array[index];
        var appName = pageToVisit.substr(pageToVisit.indexOf("store/apps/details?id=") + 22, pageToVisit.length)
        var tempApp = {}
        tempApp["weekName"] = weekName;
        tempApp["category"] = element.pathName
        tempApp["appName"] = appName
        tempApp["country"] = element.country
        tempApp["url"] = "https://play.google.com" + pageToVisit + "&hl=en&gl=" + element.country
        toProcess[indice + index] = tempApp;
    }
    fs.writeFileSync('./results/'+weekName+'/toProcess' + weekName + '.json', JSON.stringify(toProcess, null, 4), "utf8")

    if (!fs.existsSync('./results/'+weekName+'/statistics' + weekName + '.json')) {
        fs.writeFileSync('./results/'+weekName+'/statistics' + weekName + '.json', JSON.stringify([]));
    }
    var statistics = JSON.parse(fs.readFileSync('./results/'+weekName+'/statistics' + weekName + '.json', 'utf8'));
    var tempStat = {}
    tempStat["category"] = element.pathName
    tempStat["weekName"] = weekName;
    tempStat["country"] = element.country
    tempStat["amount"] = array.length
    statistics[statistics.length] = tempStat;
    fs.writeFileSync('./results/'+weekName+'/statistics' + weekName + '.json', JSON.stringify(statistics, null, 4), "utf8")
    console.log(statistics[statistics.length - 1])
    console.log(toProcess.length)
}
