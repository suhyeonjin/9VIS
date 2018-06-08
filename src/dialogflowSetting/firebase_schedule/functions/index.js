'use strict';

const {dialogflow} = require('actions-on-google');
const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp()
const app = dialogflow({debug: true});

const db = admin.database();

app.intent('pushreport', (conv,{ClassReport,datetime,ReportType}) => {
    var ref = db.ref("9vis/datasets/reports");
    var userRef = ref.child(`${ReportType}`);
    var mydeadline = `${datetime.date_time}`.substring(0,10)
    
    userRef.child(`${ClassReport}`).set({
        deadline : `${mydeadline}`,
        classtype : `${ClassReport}`
    });

    conv.close(`날짜는  ${mydeadline}`+` 과목은 ${ClassReport}` +`${ReportType}  등록 완료하였습니다`);
});


app.intent('getreport',(conv,{ReportType}) =>{
    var ref = db.ref("9vis/datasets/reports");
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

exports.ninevis = functions.https.onRequest(app);
