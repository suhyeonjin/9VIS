'use strict';
const JsonSocket = require('json-socket');
const net = require('net');
const {dialogflow} = require('actions-on-google');
const functions = require('firebase-functions');
const admin = require('firebase-admin');
const app = dialogflow({debug: true});
const myPath = "9vis/datasets/";
admin.initializeApp()
const db = admin.database();

app.intent('pushreport', (conv,{ClassReport,datetime,ReportType}) => {
    var ref = db.ref(myPath + "reports");
    var userRef = ref.child(`${ReportType}`);
    var mydeadline = `${datetime.date_time}`.substring(0,10)
    
    userRef.child(`${ClassReport}`).set({
        deadline : `${mydeadline}`,
        classtype : `${ClassReport}`
    });

    conv.close(`날짜는  ${mydeadline}`+` 과목은 ${ClassReport}` +`${ReportType}  등록 완료하였습니다`);
});

app.intent('getreport',(conv,{ReportType}) =>{
    var ref = db.ref(myPath + "reports");
    var userRef = ref.child(`${ReportType}`);

    return userRef.once('value').then(function(snapshot) {

        return snapshot.forEach(function(childSnapshot){
            var myclass = childSnapshot.key; 
            var mydeadline = childSnapshot.child("deadline").val()
            conv.close(`${mydeadline} 까지  ${myclass} 과제가  있습니다`);
            return;
        });

    });
});

app.intent('askMenu',(conv,{structure, menucheck}) =>{


    var ref = db.ref(myPath + "structure/"+`${structure}`);
    var userRef = ref.child(`${menucheck}`);
    return userRef.once('value').then(function(snapshot) {
        snapshot.forEach(function(childSnapshot){
            var key = childSnapshot.key;
            var item = childSnapshot.val();
            conv.close(`${structure}`+"의 "+`${menucheck}`+"메뉴입니다. "+ `${key}`+"은 "+`${item}`+" 입니다.");
            //return;
        });
        return;

    });

});

exports.ninevis = functions.https.onRequest(app);
