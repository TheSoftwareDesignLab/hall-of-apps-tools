var request = require('request');
var fs = require('fs');
var CronJob = require('cron').CronJob;
var weekName =  "20180826-20180901"//getWeekName();//
var interval = 2;

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


var job = new CronJob('*/'+interval+' * * * * *', function() {
    if (!fs.existsSync('./results/'+weekName+'/toProcess'+weekName+'.1.json')) {
        fs.copyFileSync('./results/'+weekName+'/toProcess'+weekName+'.json','./results/'+weekName+'/toProcess'+weekName+'.1.json')
        // var obj = JSON.parse(fs.readFileSync('./results/'+weekName+'/toProcess'+weekName+'.json', 'utf8'));
        // fs.writeFileSync('./results/'+weekName+'/toProcess'+weekName+'.1.json', JSON.stringify(obj, null, 4));
    }
    var toDo = JSON.parse(fs.readFileSync('./results/'+weekName+'/toProcess'+weekName+'.1.json', 'utf8'));
    if(toDo.length==0){
        fs.unlinkSync('./results/'+weekName+'/toProcess'+weekName+'.1.json')
        job.stop()
    } else {
        var tryy = 1;
        var element = toDo[0]
        var originalTime = (new Date()).getTime();
        console.log("appsFaltantes: "+toDo.length)
        console.log("INFO: retrieving of "+ element.appName+" is about to start")
        retrievePage(element, tryy, originalTime, toDo);
    }
}, null, true, 'America/Los_Angeles');

function retrievePage(element, tryy, originalTime, toDo){
    if (!fs.existsSync("../data/"+weekName)){
        fs.mkdirSync("../data/"+weekName)
    }
    if (!fs.existsSync('./results/'+weekName+'/pending'+weekName+'.json')) {
        fs.writeFileSync('./results/'+weekName+'/pending'+weekName+'.json', JSON.stringify([]));
    }
    request(element.url, function(error, response, body) {
        if(error && tryy < 11) {
            console.log("WARNING: retrieving "+element.url+" - error: "+error.message)
            var petitionTime = (new Date()).getTime()
            while((petitionTime-originalTime)<((interval*1000)/10)){
                petitionTime = (new Date()).getTime();
            }
            console.log("INFO: retrieving "+element.url+" - "+(tryy+1)+" try, on time: "+petitionTime)
            retrievePage(element, tryy+1, petitionTime, toDo)
        } else if(response.statusCode !== 200) {
            console.log("Error: app "+element.appName+" was not retrieved succesfully - statusCode: "+response.statusCode)
            var obj = JSON.parse(fs.readFileSync('./results/'+weekName+'/pending'+weekName+'.json', "utf8"));
            obj[obj.length]=element;
            fs.writeFileSync('./results/'+weekName+'/pending'+weekName+'.json',JSON.stringify(obj,null,4),"utf8")
            console.log("INFO: New toRetrieve task has been added: "+ JSON.stringify(obj[obj.length-1]))
            var newArray = toDo.slice(1,toDo.length)
            fs.writeFileSync('./results/'+weekName+'/toProcess'+weekName+'.1.json', JSON.stringify(newArray, null, 4));
        } else if(response.statusCode === 200) {
            console.log("SUCESS: app "+element.appName+" was retrieved succesfully")
            fs.writeFileSync("../data/"+weekName+"/"+element.weekName+"%"+element.country+"%"+element.category+"%"+element.appName+".html",body,"utf8");
            var newArray = toDo.slice(1,toDo.length)
            fs.writeFileSync('./results/'+weekName+'/toProcess'+weekName+'.1.json', JSON.stringify(newArray, null, 4));
        } else {
            // the url content was unable to get after 10 tries
            console.log("ERROR: retrieving "+element.url+" fails, after 10 tries the content was unable to be retrieved")
            // The url is added to unretrieved urls file 
            var obj = JSON.parse(fs.readFileSync('./results/'+weekName+'/pending'+weekName+'.json', "utf8"));
            obj[obj.length]=element;
            fs.writeFileSync('./results/'+weekName+'/pending'+weekName+'.json',JSON.stringify(obj,null,4),"utf8")
            console.log("INFO: New toRetrieve task has been added: "+ JSON.stringify(obj[obj.length-1]))
            var newArray = toDo.slice(1,toDo.length)
            fs.writeFileSync('./results/'+weekName+'/toProcess'+weekName+'.1.json', JSON.stringify(newArray, null, 4));
        }
    });
}
